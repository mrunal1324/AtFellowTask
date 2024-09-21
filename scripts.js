document.addEventListener('DOMContentLoaded', () => {
    // Handle Login Form Submission
    document.getElementById('login-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            if (response.ok) {
                localStorage.setItem('token', data.token);
                alert('Login successful!');
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Handle Itinerary Form Submission
    document.getElementById('itinerary-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const token = localStorage.getItem('token');
        if (!token) {
            alert('Please log in first!');
            return;
        }

        const destination = document.getElementById('destination').value;
        const duration = document.getElementById('duration').value;
        const budget = document.getElementById('budget').value;
        const interests = document.getElementById('interests').value;

        try {
            const response = await fetch('/itinerary', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-token': token,
                },
                body: JSON.stringify({ destination, duration, budget, interests, user_id: 'test_user' }), // replace 'test_user' with actual user ID
            });
            const data = await response.json();
            if (response.ok) {
                document.getElementById('itinerary-output').innerText = `Optimized Itinerary: ${data.itinerary.join(', ')}`;
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Handle Expense Form Submission
    document.getElementById('expense-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const amount = document.getElementById('amount').value;
        const currency = document.getElementById('currency').value;

        // Assuming a simple expense tracking endpoint for illustration
        try {
            const response = await fetch('/track-expense', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ amount, currency }),
            });
            const data = await response.json();
            if (response.ok) {
                alert(`Total Expense: ${data.total_expense}`);
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Handle Review Form Submission
    document.getElementById('review-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const token = localStorage.getItem('token');
        if (!token) {
            alert('Please log in first!');
            return;
        }

        const activityId = document.getElementById('activity-id').value;
        const rating = document.getElementById('rating').value;
        const reviewText = document.getElementById('review-text').value;

        try {
            const response = await fetch('/submit-review', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-access-token': token,
                },
                body: JSON.stringify({ activity_id: activityId, rating, review_text: reviewText }),
            });
            const data = await response.json();
            if (response.ok) {
                alert('Review submitted successfully!');
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Handle AI Chatbot Interaction
    document.getElementById('chat-submit').addEventListener('click', async () => {
        const query = document.getElementById('chat-input').value;
        try {
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            });
            const data = await response.json();
            if (response.ok) {
                document.getElementById('chat-output').innerText = `Assistant: ${data.response}`;
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});
