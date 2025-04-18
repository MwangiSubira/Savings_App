// frontend/src/utils/validators.js
export const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
  };
  
  export const validatePhone = (phone) => {
    const re = /^\+?[\d\s-]{10,15}$/;
    return re.test(phone);
  };
  
  export const validatePassword = (password) => {
    const minLength = 8;
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[^A-Za-z0-9]/.test(password);
  
    return {
      isValid: password.length >= minLength && hasUpper && hasLower && hasNumber && hasSpecial,
      requirements: {
        minLength,
        hasUpper,
        hasLower,
        hasNumber,
        hasSpecial,
      },
    };
  };
  
  export const validateAmount = (amount) => {
    return !isNaN(amount) && parseFloat(amount) > 0;
  };
  
  export const validateDate = (dateString) => {
    return !isNaN(Date.parse(dateString));
  };