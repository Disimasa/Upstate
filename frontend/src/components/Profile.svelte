<script>
import { fly, fade } from 'svelte/transition';
let direction = -1;
let change = 0;
let slide = 0;
let current_status = 'Ботаю';
let statuses = ['Ботаю', 'Чилю', 'Сплю', 'Играю', 'Отошел', 'qwe','sdd2', 'dsdsd', '1dsds','dsds', 'sad', 'sdd'];
function next_slide() {
    if (statuses.length > 5) {
        slide++;
        if (slide*5 >= statuses.length) {
            slide = 0;
        }
    if (change === 0) {
        direction = -1;
            change = 1;
        } else {
        direction = 1;
            change = 0
        }
    }
}
function previous_slide() {
    if (statuses.length > 5) {
        if (slide > 0) {
            slide--;
        } else {
            slide = Math.floor(statuses.length / 6);
        }
        if (change === 0) {
            direction = 1;
            change = 1;
        } else {
            direction = -1;
            change = 0
        }
    }
}
</script>
<style>
.picture {
        grid-area: picture;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .circle {
        width: 159px;
        height: 159px;
        border-radius: 79px;
        background: url('/logo.svg') center;
        background-size: cover;
        box-shadow: 0 4px 17px rgba(0, 0, 0, 0.03);
    }
    .info {
        grid-area: info;
    }

    ul {
        list-style-type: none;
    }

    ul p {
        display: inline-block;
    }
    .current_status {
        display: flex;
        align-items: center;
        grid-area: current_status;
        font-size: 2em;
    }
    .current_status p, .new_status p {
        font-family: 'Comfortaa', cursive;
    }
    .status {
        color: #30919E;
    }
    .name, .surname, .job {
        border-bottom: 3px solid #939DFF;
        margin: 0;
        display: inline-block;
        font-family: 'Comfortaa', cursive;
    }
    .button_left {
    grid-area: button_left;
    display: flex;
    justify-content: center;
    align-items: center;
}
.status_row_1 {
    grid-area: status_row_1;
}
.status_row_2 {
    grid-area: status_row_2;
}
.status_row_1, .status_row_2 {
    display: flex;
    justify-content: space-around;
    align-items: center;
}
.button_status {
    border-radius: 30px;
    background: #FFFFFF;
    flex: auto;
    width: 70%;
    padding: 15px 15px;
    margin: 20px 3%;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.09);
    border: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Comfortaa', cursive;
}
.button_right {
    grid-area: button_right;
    display: flex;
    justify-content: center;
    align-items: center;
}
.arrow {
    width: 50px;
    height: 50px;
    background: #FFFFFF;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.11);
    border-radius: 79px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.arrow:hover {
    cursor:pointer;
}
.arrow_image {
    width: 20px;
    height: 30px;
}
@media all and (max-width: 780px) {
    .component {
        position: absolute;
        top: 0;
        left: 0;
        height: 2000px;
        width: 100%;
        background-color: #FFFFFF;
        z-index: 0;
        padding: 0;
        margin: 0;
    }
    .card {
        width: 93%;
        background: #FFFFFF;
        border-radius: 30px;
        margin: 50px 0 0 15px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.09);
        display: grid;
        grid-template-rows: repeat(4, auto);
        grid-template-areas: "picture"
    "info"
    "current_status"
    "new_status";
    }
    .circle {
        margin: 10px 0 0 0;
    }
    .info {
        text-align: center;
    }
    ul {
        padding: 0;
    }
    ul p {
        color: #6B5581;
        margin: 7px;
        font-size: 20px;

    }
    .current_status {
        justify-content: center;
        margin: 0;
        font-size: 6vw;
    }
    .all_line {
        display: none;
    }
    .status {
        font-size: 10vw;
        margin: 0 0 0 30px;
    }
    .new_status {
        grid-area: new_status;
        color: #717171;
        font-size: 6vw;
        text-align: center;
    }
     .input_new_status {
     display: none;
     }
     .status_row_1, .status_row_2 {
         display: flex;
         flex-direction: column;
     }
.statuses {
    display: grid;
    grid-template-columns: 10px 50px 1fr 50px 10px;
    grid-template-rows: repeat(2, auto);
    grid-template-areas:
            ". button_left status_row_1 button_right ."
    ". button_left status_row_2 button_right .";
}
}
@media all and (min-width: 1100px) {
     .input_new_status {
     font-size: 16px;
     }
}
@media all and (max-width: 1100px) {
     .input_new_status {
     font-size: 1.5vw;
     }
}
@media all and (min-width: 780px){
    .component {
        width: 100%;
        height: 500px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 100px;
    }

    .card {
        height: 400px;
        width: 95%;
        max-width: 1300px;
        background-color: #FBFBFB;
        box-shadow: 4px 4px 30px rgba(0, 0, 0, 0.07);
        border-radius: 28px;
        display: grid;
        grid-template-columns: 200px 1fr;
        grid-template-rows: 100px 100px 1fr;
        grid-template-areas: "picture current_status" "picture new_status" "info statuses";
    }
    .current_status p {
        margin: 50px 0 -10px 10px;
    }
    .new_line {
        display: none;
    }
    .new_status {
        grid-area: new_status;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .new_status p {
        font-size: 2vw;
        color: #717171;
        margin: 0 0 0 32px;
    }

    .input_new_status {
        font-family: 'Comfortaa', cursive;
        font-style: normal;
        font-weight: normal;
        color: #6574FF;
        outline: none;
        border: 0;
        border-bottom: 2px solid #939DFF;
        width: 200px;
        background-color: #FBFBFB;
        margin: 0 50px;
    }
input::-moz-placeholder {
    color: #6574FF; }
input::-webkit-input-placeholder { color: #6574FF; }
ul p {
    margin: 10px 0 5px 0;
}
    .statuses {
        width: 100%;
        grid-area: statuses;
        display: grid;
        grid-template-columns: 50px 1fr 50px 50px;
        grid-template-rows: 1fr 1fr;
        grid-template-areas:
    "button_left status_row_1 button_right ."
    "button_left status_row_2 button_right .";
    }
.button_status {
    border-radius: 30px;
    background: #FFFFFF;
    flex: auto;
    max-width: 200px;
    padding: 15px 15px;
    margin: 0 3%;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.09);
    border: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Comfortaa', cursive;
}
.button_status:hover {
    cursor: pointer;
}
.current_button {
    color: #6574FF;
}
}
</style>
<div class="component">
<div class="card" out:fade="{{duration: 500}}">
<div class="picture"><div class="circle"></div></div>
    <div class="current_status"><p class="new_line">Текущий<br/> статус: </p><p class="all_line">Текущий статус:</p><p class="status">{current_status}</p></div>
<div class="new_status"><p>Выбери новый статус</p><input type="text" placeholder="Добавь свой" class="input_new_status"></div>
<div class="info">
    <ul>
    <li><div class="name"><p>Иван</p></div></li>
    <li><div class="name"><p>Иванов</p></div></li>
    <li><div class="job"><p>Разработчик</p></div></li>
    </ul>
</div>
<div class="statuses">
    <div class="button_left"><div class="arrow" on:click={previous_slide}><img class="arrow_image" src="Left.png" alt=""> </div></div>
    {#if change === 0}
    <div class="status_row_1" in:fly="{{ x: 100*direction, duration: 100 }}">
        {#each statuses as status, i}
            {#if i>slide*5-1 && i<slide*5+3}
            <button class="button_status {current_status === status ? 'current_button':''}" on:click={() => current_status = status}>{status}</button>
                {/if}
            {/each}
    </div>
    <div class="status_row_2" in:fly="{{ x: (100*direction), duration: 100 }}">
        {#each statuses as status, i}
            {#if i>slide*5+2 && i<slide*5+5}
            <button class="button_status {current_status === status ? 'current_button':''}" on:click={() => current_status = status}>{status}</button>
                {/if}
            {/each}
    </div>
        {:else}
    <div class="status_row_1" in:fly="{{ x: -100*direction, duration: 100}}">
        {#each statuses as status, i}
            {#if i>slide*5-1 && i<slide*5+3}
            <button class="button_status {current_status === status ? 'current_button':''}" on:click={() => current_status = status}>{status}</button>
                {/if}
            {/each}
    </div>
    <div class="status_row_2" in:fly="{{ x: -100*direction, duration: 100 }}">
        {#each statuses as status, i}
            {#if i>slide*5+2 && i<slide*5+5}
            <button class="button_status {current_status === status ? 'current_button':''}" on:click={() => current_status = status}>{status}</button>
                {/if}
            {/each}
    </div>
        {/if}
    <div class="button_right"><div class="arrow" on:click={next_slide}><img class="arrow_image" src="/Right.png" alt=""> </div></div>
</div>
</div>
</div>
