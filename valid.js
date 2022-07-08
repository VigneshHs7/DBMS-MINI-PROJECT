	//Validtion Code For Inputs

	var ID = document.forms['form']['ID'];
	var password = document.forms['form']['password'];

	var id_error = document.getElementById('ID_error');
	var pass_error = document.getElementById('pass_error');

	id.addEventListener('number', ID_Verify);
	password.addEventListener('textInput', pass_Verify);

	function validated() {
	    if (email.value.length < 9) {
	        email.style.border = "1px solid red";
	        email_error.style.display = "block";
	        email.focus();
	        return false;
	    }
	    if (password.value.length < 6) {
	        password.style.border = "1px solid red";
	        pass_error.style.display = "block";
	        password.focus();
	        return false;
	    }

	}

	function ID_Verify() {
	    if (ID_Verify.value.length >= 8) {
	        ID_Verify.style.border = "1px solid silver";
	        ID_Verify.style.display = "none";
	        return true;
	    }
	}

	function pass_Verify() {
	    if (password.value.length >= 5) {
	        password.style.border = "1px solid silver";
	        pass_error.style.display = "none";
	        return true;
	    }
	}