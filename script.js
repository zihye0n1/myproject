document.getElementById('addTodo').addEventListener('click', function() {
    const dateInput = document.getElementById('dateInput');
    const todoInput = document.getElementById('todoInput');
    const selectedDate = dateInput.value;
    const todoText = todoInput.value.trim();

    if (selectedDate && todoText) {
        const todoList = document.getElementById('todoList');
        const li = document.createElement('li');
        li.textContent = `${selectedDate}: ${todoText}`;

        const deleteButton = document.createElement('button');
        deleteButton.textContent = '삭제';
        deleteButton.onclick = function() {
            li.remove();
            saveTodos();
        };

        li.appendChild(deleteButton);
        todoList.appendChild(li);
        todoInput.value = ''; // 입력란 비우기
        saveTodos(); // 할 일을 저장
    } else {
        alert('날짜와 할 일을 입력해주세요!');
    }
});

// 로컬 저장소에서 할 일 목록 불러오기
function loadTodos() {
    const todos = JSON.parse(localStorage.getItem('todos')) || [];
    todos.forEach(todo => {
        const todoList = document.getElementById('todoList');
        const li = document.createElement('li');
        li.textContent = `${todo.date}: ${todo.text}`;

        const deleteButton = document.createElement('button');
        deleteButton.textContent = '삭제';
        deleteButton.onclick = function() {
            li.remove();
            saveTodos();
        };

        li.appendChild(deleteButton);
        todoList.appendChild(li);
    });
}

function saveTodos() {
    const todoList = document.getElementById('todoList');
    const todos = [];
    for (let i = 0; i < todoList.children.length; i++) {
        const li = todoList.children[i];
        const [date, text] = li.textContent.split(': ');
        todos.push({ date, text: text.replace('삭제', '').trim() });
    }
    localStorage.setItem('todos', JSON.stringify(todos));
}

// 페이지 로드 시 할 일 목록 불러오기
window.onload = loadTodos;
