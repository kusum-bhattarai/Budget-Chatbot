document.addEventListener('DOMContentLoaded', () => {
    const pages = document.querySelectorAll('.page');
    const expenseForm = document.getElementById('expense-form');
    const savingsForm = document.getElementById('savings-form');
    const budgetForm = document.getElementById('budget-form');
    const balanceForm = document.getElementById('balance-form');
    const expenseList = document.getElementById('expense-list');
    const expenseChart = document.getElementById('expense-chart').getContext('2d');
    const expensePieChart = document.getElementById('expense-pie-chart').getContext('2d');
    let expenses = JSON.parse(localStorage.getItem('expenses')) || [];
    let budget = parseFloat(JSON.parse(localStorage.getItem('budget'))) || 1000;
    let bankBalance = parseFloat(JSON.parse(localStorage.getItem('bankBalance'))) || 5000;
    let creditCardBalance = parseFloat(JSON.parse(localStorage.getItem('creditCardBalance'))) || 1000;
    let savingsGoal = parseFloat(JSON.parse(localStorage.getItem('savingsGoal'))) || 0;
    let amountSaved = parseFloat(JSON.parse(localStorage.getItem('amountSaved'))) || 0;

    const showPage = (pageId) => {
        console.log(`Switching to page: ${pageId}`);
        pages.forEach(page => {
            if (page.id === pageId) {
                page.classList.add('active');
            } else {
                page.classList.remove('active');
            }
        });
    };

    document.getElementById('dashboard-button').addEventListener('click', () => showPage('dashboard'));
    document.getElementById('expense-entry-button').addEventListener('click', () => showPage('expenseEntry'));

    const updateLocalStorage = () => {
        localStorage.setItem('expenses', JSON.stringify(expenses));
        localStorage.setItem('budget', JSON.stringify(budget));
        localStorage.setItem('bankBalance', JSON.stringify(bankBalance));
        localStorage.setItem('creditCardBalance', JSON.stringify(creditCardBalance));
        localStorage.setItem('savingsGoal', JSON.stringify(savingsGoal));
        localStorage.setItem('amountSaved', JSON.stringify(amountSaved));
    };

    const updateExpenseList = () => {
        console.log('Updating expense list:', expenses);
        expenseList.innerHTML = expenses.map((expense, index) => `
            <div class="expense-item">
                <span>${expense.description} - ${expense.category} - $${expense.amount} (${expense.paymentMethod})</span>
                <button class="delete-button" data-index="${index}">Delete</button>
            </div>
        `).join('');
        updateExpenseChart();
        updateExpensePieChart();
        document.getElementById('monthly-budget-display').innerText = `Monthly Budget: $${budget}`;
        document.getElementById('bank-balance-display').innerText = `Bank Balance: $${bankBalance}`;
        document.getElementById('credit-card-balance-display').innerText = `Credit Card Balance: $${creditCardBalance}`;
        attachDeleteHandlers();
    };

    const attachDeleteHandlers = () => {
        document.querySelectorAll('.delete-button').forEach(button => {
            button.addEventListener('click', (e) => {
                const index = e.target.dataset.index;
                const expense = expenses[index];
                if (expense.paymentMethod === 'bank') {
                    bankBalance += parseFloat(expense.amount);
                } else if (expense.paymentMethod === 'creditCard') {
                    creditCardBalance -= parseFloat(expense.amount);
                }
                budget += parseFloat(expense.amount);
                expenses.splice(index, 1);
                updateLocalStorage();
                updateExpenseList();
            });
        });
    };

    const updateExpenseChart = () => {
        const categories = expenses.reduce((acc, expense) => {
            acc[expense.category] = (acc[expense.category] || 0) + parseFloat(expense.amount);
            return acc;
        }, {});

        const data = {
            labels: Object.keys(categories),
            datasets: [{
                label: 'Expenses',
                data: Object.values(categories),
                backgroundColor: 'rgba(75,192,192,0.4)',
                borderColor: 'rgba(75,192,192,1)',
            }]
        };

        new Chart(expenseChart, {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    };

    const updateExpensePieChart = () => {
        const categories = expenses.reduce((acc, expense) => {
            acc[expense.category] = (acc[expense.category] || 0) + parseFloat(expense.amount);
            return acc;
        }, {});

        const data = {
            labels: Object.keys(categories),
            datasets: [{
                data: Object.values(categories),
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'],
            }]
        };

        new Chart(expensePieChart, {
            type: 'pie',
            data: data,
            options: {
                responsive: true
            }
        });
    };

    expenseForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const amount = parseFloat(document.getElementById('amount').value);
        const category = document.getElementById('category').value;
        const description = document.getElementById('description').value;
        const paymentMethod = document.getElementById('payment-method').value;

        const expense = { amount, category, description, paymentMethod };
        console.log('Adding expense:', expense);
        expenses.push(expense);

        if (paymentMethod === 'bank') {
            bankBalance -= amount;
        } else if (paymentMethod === 'creditCard') {
            creditCardBalance += amount;
        }

        budget -= amount;

        updateLocalStorage();
        updateExpenseList();
        document.getElementById('bank-balance-display').innerText = `Bank Balance: $${bankBalance}`;
        document.getElementById('credit-card-balance-display').innerText = `Credit Card Balance: $${creditCardBalance}`;
        expenseForm.reset();
    });

    savingsForm.addEventListener('submit', (e) => {
        e.preventDefault();
        savingsGoal = parseFloat(document.getElementById('savings-goal').value);
        amountSaved = parseFloat(document.getElementById('amount-saved').value);
        document.getElementById('savings-goal-display').innerText = `Savings Goal: $${savingsGoal}`;
        updateLocalStorage();
    });

    budgetForm.addEventListener('submit', (e) => {
        e.preventDefault();
        budget = parseFloat(document.getElementById('monthly-budget').value);
        document.getElementById('monthly-budget-display').innerText = `Monthly Budget: $${budget}`;
        updateLocalStorage();
    });

    balanceForm.addEventListener('submit', (e) => {
        e.preventDefault();
        bankBalance = parseFloat(document.getElementById('bank-balance').value);
        creditCardBalance = parseFloat(document.getElementById('credit-card-balance').value);
        updateLocalStorage();
        document.getElementById('bank-balance-display').innerText = `Bank Balance: $${bankBalance}`;
        document.getElementById('credit-card-balance-display').innerText = `Credit Card Balance: $${creditCardBalance}`;
    });

    document.getElementById('bank-balance').value = bankBalance;
    document.getElementById('credit-card-balance').value = creditCardBalance;
    document.getElementById('bank-balance-display').innerText = `Bank Balance: $${bankBalance}`;
    document.getElementById('credit-card-balance-display').innerText = `Credit Card Balance: $${creditCardBalance}`;
    document.getElementById('savings-goal-display').innerText = `Savings Goal: $${savingsGoal}`;
    document.getElementById('monthly-budget-display').innerText = `Monthly Budget: $${budget}`;

    showPage('dashboard');
    updateExpenseList();
});
