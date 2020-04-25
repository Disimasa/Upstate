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
		const todo = {
			id: uid++,
			done: false,
			description: input.value
		};

		tasks = [todo, ...tasks];
		input.value = '';
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
.component {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #E5E5E5;
        margin-bottom: 200px;
    }
@media all and (max-width: 780px) {

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
        font-family: 'Comfortaa', cursive;
        font-size: 20px;
    }

    .tasks, .performed {
    }

    .tasks {

    }

    .tasks p, .performed p {
        margin: 30px 0 40px 30px;
    }

    .performed {

    }

    .task_block {
        padding: 10px 20px;
        border-radius: 30px;
        margin: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.09);
        text-align: center;
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

    .task_text p, .performed_text p {
        padding-bottom: 2px;
        margin: 0;
    }

    .performed_text {
        border-bottom: 2px solid #2FFF9B;
    }
}
</style>
<div class="component">
<div class="board" out:fade="{{duration: 500}}">
    <div class="tasks">
<p>Рабочие задачи</p>
        {#each tasks.filter(t => !t.done) as todo (todo.id)}
        <div class="task_block" on:click={() => mark(todo, true)} in:receive="{{key: todo.id}}"
				out:send="{{key: todo.id}}"
				animate:flip>
            <div class="task_text"><p>{todo.description}</p></div>
        </div>
		{/each}
    </div>
    <div class="performed">
        <p>Завершенные задачи</p>
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
