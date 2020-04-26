<script>
import { quintOut } from 'svelte/easing';
import { crossfade } from 'svelte/transition';
import { flip } from 'svelte/animate';
import { fade } from 'svelte/transition';
let uid = 1;
let tasks =  [
		{ id: uid++, done: false, description: 'написать что-нибудь в документацию' },
		{ id: uid++, done: false, description: 'начать писать статью в блог' },
		{ id: uid++, done: true, description: 'купить молока' },
		{ id: uid++, done: false, description: 'покосить газон' },
		{ id: uid++, done: false, description: 'покормить черепашку' },
		{ id: uid++, done: false, description: 'пофиксить пару багов' },
	];
	const [send, receive] = crossfade({
		duration: d => Math.sqrt(d * 200),

		fallback(node, params) {
			const style = getComputedStyle(node);
			const transform = style.transform === 'none' ? '' : style.transform;

			return {
				duration: 600,
				easing: quintOut,
				css: t => `
					transform: ${transform} scale(${t});
					opacity: ${t}
				`
			};
		}
	});
function add(input) {
    if (input.value !== '') {
        const todo = {
            id: uid++,
            done: false,
            description: input.value
        };

        tasks = [...tasks, todo];
        input.value = '';
    }
}

	function remove(todo) {
		tasks = tasks.filter(t => t !== todo);
	}

	function mark(todo, done) {
		todo.done = done;
		remove(todo);
		tasks = tasks.concat(todo);
	}
</script>
<style>
    input::-moz-placeholder {
    color: #6574FF;}
input::-webkit-input-placeholder { color: #6574FF;}
.component {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #E5E5E5;
        margin-bottom: 200px;
        font-family: 'Comfortaa', cursive;
    }
.task_block:hover {
        cursor: pointer;
        background-color: #E5E5E5;
    }

    .task_text, .performed_text {
        display: inline-block;
    }

    .task_text {
        display: inline-block;
        border-bottom: 2px solid #939DFF;
    }
    .performed_text {
        border-bottom: 2px solid #2FFF9B;
    }
    .input_task_block {
    font-family: Comfortaa, cursive;
    padding: 10px 20px;
    margin: 20px;
    width: inherit;
    border:0;
    border-radius: 30px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.09);
    outline: none;
}
@media all and (max-width: 780px) {
    .component {
        background-color: #FFFFFF;
    }
.board {
    width: 93%;
    margin: 10px 0 0 0;
    background-color: #FFFFFF;
}
.tasks {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.tasks p, .performed p {
    font-size: 8vw;
    color: #4B4B4B;
    text-align: center;
}
.task_text p, .performed_text p {
    font-size: 4vw;
    margin:0 0 5px 0;
}
.task_block {
        padding: 5px 20px;
        border-radius: 30px;
        margin: 15px 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.09);
        text-align: center;
    }
.input_task_block {
    text-align: center;
    width: 60%;
    font-size: 20px;
}
}
@media all and (min-width: 780px) {
    .board {
        width: 95%;
        max-width: 1300px;
        background-color: #FBFBFB;
        box-shadow: 4px 4px 30px rgba(0, 0, 0, 0.07);
        border-radius: 28px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        font-size: 20px;
    }
    .tasks p, .performed p {
        margin: 30px 0 40px 30px;
    }

    .task_text p, .performed_text p {
        padding-bottom: 2px;
        margin: 0;
    }
.task_block {
        padding: 10px 20px;
        border-radius: 30px;
        margin: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.09);
        text-align: center;
    }
}
</style>
<div class="component" transition:fade="{{duration: 300}}">
<div class="board">
    <div class="tasks">
<p>Рабочие задачи</p>
        {#each tasks.filter(t => !t.done) as todo (todo.id)}
        <div class="task_block" on:click={() => mark(todo, true)} in:receive="{{key: todo.id}}"
				out:send="{{key: todo.id}}"
				animate:flip>
            <div class="task_text"><p>{todo.description}</p></div>
        </div>
		{/each}
    <input class="input_task_block" placeholder="Добавить задачу" on:keydown={e => e.which === 13 && add(e.target)}>
    </div>
    <div class="performed">
        <p>Принятые задачи</p>
        {#each tasks.filter(t => t.done) as todo (todo.id)}
        <div class="task_block" on:click={() => mark(todo, false)} in:receive="{{key: todo.id}}"
				out:send="{{key: todo.id}}"
				animate:flip="{{duration: 200}}">
            <div class="performed_text"><p>{todo.description}</p></div>
        </div>
		{/each}
    </div>
</div>
</div>
