function createQues() {
	const formToReset = document.getElementById("quiz");
	formToReset.reset();
}

function add_quiz() {
	const br = document.createElement('br');

	const form = document.createElement('form');
	form.setAttribute("method","post");

	const quizname =  document.createElement('input');
	quizname.setAttribute("type","text");
	quizname.setAttribute("name","quizname");
	quizname.setAttribute("placeholder","Enter quizname...");

	const quizsubmit = document.createElement('input');
	quizsubmit.setAttribute('type','submit');
	quizsubmit.setAttribute('value','Submit');

	form.appendChild(quizname);
	form.appendChild(quizsubmit);

	document.getElementById('quiz-container').appendChild(form);


}


