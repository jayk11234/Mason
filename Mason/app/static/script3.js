//script for user.html

function add_quiz() {
	const br = document.createElement('br');

	let addQuiz = document.querySelector('#add-btn');
	addQuiz.style.display = 'none';
	const form = document.createElement('form');
	form.setAttribute("method","post");
	form.setAttribute("required","required")

	const quizname =  document.createElement('input');
	quizname.setAttribute("type","text");
	quizname.setAttribute("name","quizname");
	quizname.setAttribute("placeholder","Enter quizname...");
	quizname.setAttribute('id','quiz-name')

	const submitBtn = document.createElement('input');
	submitBtn.setAttribute('type','submit');
	submitBtn.setAttribute('value','Submit');
	submitBtn.setAttribute('id','submit-btn');
	
	let closeBtn = document.createElement('button');
	closeBtn.innerHTML='&times;'
	closeBtn.setAttribute('id','close-btn')

	form.appendChild(quizname);
	form.appendChild(submitBtn);
	form.appendChild(closeBtn);

	document.getElementById('quiz-container').appendChild(form);
	
	submitBtn.addEventListener('click',function(event){
		if(quizname.value!==""){
		addQuiz.style.display='block';
		form.style.display='none';
		}
		else{
			event.preventDefault()
			quizname.placeholder="Please enter quizname!";

		}
	})
	closeBtn.addEventListener('click',function(){
		form.remove();
		addQuiz.style.display='block';

	})

		
	

	
}
