function toggleForm() {
    const loginContainer = document.querySelector('.login-container');
    const signupContainer = document.querySelector('.signup-container');

    if (signupContainer.style.display === 'none') {
        loginContainer.style.display = 'none';
        signupContainer.style.display = 'block';
    } else {
        loginContainer.style.display = 'block';
        signupContainer.style.display = 'none';
    }
}
