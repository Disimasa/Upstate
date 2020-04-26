<script>
import { fade, slide } from 'svelte/transition';
import { onMount } from 'svelte';
import {url} from '../../static/site_url.js';
let team;
let bool_arr;
onMount(fetch_data);
async function fetch_data() {
        let token = localStorage.getItem('team_token');
        const resp = await fetch(url + 'show/team?' + new URLSearchParams({'public_token': token}));
        const json = await resp.json();
        team = json['team']['name'];
        bool_arr= [];
        for (let i = 0; i < json['members'].length; i++) {
        bool_arr[i] = {i: 0};
        }
        return json;
    }
    let json = fetch_data();
function drop(num) {
    if (bool_arr[num] === '0') {
        bool_arr[num] = '1';
    } else {
        bool_arr[num] = '0';
    }
}
</script>
<style>
    .member_box {
    width: 600px;
    background: #FFFFFF;
    border-radius: 30px;
    margin: 50px 25px 0 25px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.09);
    font-family: 'Comfortaa', cursive;
    flex: 0 0 600px;
}
    .info {
    grid-area: info;
    padding-top: 10px;
}
    .job_text {
    display: inline-block;
    border-bottom: 2px solid #939DFF;
}
    .tasks {
    background: #6573FE;
    border-radius: 30px;
    padding: 10px 50px;
    color: #FFFFFF;
    text-align: center;
    flex: 1 1;
}
    .arrow {
    height: 22px;
    width: 100%;
    text-align: center;
    grid-area: arrow;
        margin: 5px 0;
}
.arrow_image {
    width: 38px;
    height: 13px;
}
.arrow_image:hover {
    cursor: pointer;
}
.transformed_arrow {
    transform: rotate(180deg);
}
@media all and (max-width: 780px) {
    .component {
        width: 100%;
        margin-bottom: 200px;
    }
    .team {
        width: 93%;
        background: #FFFFFF;
        border-radius: 30px;
        margin: 50px 0 10px 15px;
        padding: 10px 0 100px 0;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.09);
    }
    .member_box {
        width: 82%;
        max-width: 500px;
    }
    .member {
        display: grid;
        grid-template-rows: repeat(4, auto);
        grid-template-areas:
    "info"
    "job"
    "current_status"
    "current_task";
    }
    .info p {
        font-size: 30px;
        margin: 10px 0 0 20px;
    }
    .job {
        grid-area: job;
        margin: 0 0 0 20px;
    }
    .job_text p {
        margin: 0 0 6px 0;
    }
    .status {
        margin: 0 0 0 20px;
    }
    .status p{
        font-size: 20px;
        margin: 10px 0 5px 0;
    }
    .current_status {
        grid-area: current_status;
        background: #6574FF;
        border-radius: 30px;
        padding: 7px 0;
        margin: 0 30px 0 0;
        max-width: 250px;
        text-align: center;
        color: #FFFFFF;
}
    .task {
        margin: 0 0 0 20px;
    }
    .task p {
        font-size: 20px;
        margin: 10px 0 5px 0;
    }
    .current_task {
        grid-area: current_task;
        margin: 0 20px 10px 0;
        background: #6573FE;
        border-radius: 30px;
        padding: 7px 5px;
        color: #FFFFFF;
        text-align: center;
    }
    .tasks {
        margin: 0 20px 10px 20px;
    }
}
    @media all and (min-width: 780px) {
.component {
    position: absolute;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #E5E5E5;
        margin-bottom: 200px;
        margin-top: 100px;
}
.team {
        width: 90%;
        max-width: 1300px;
        background-color: #F9F9F9;
        box-shadow: 4px 4px 30px rgba(0, 0, 0, 0.07);
        border-radius: 28px;
        display: flex;
        flex-direction: row;
        align-items: center;
        padding-bottom: 50px;
        flex-wrap: wrap;
        justify-content: flex-start;
}
.member_box {
    width: 600px;
}
.member {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: repeat(3, auto);
    grid-template-areas:
    "info status"
    "job status"
    "task task"
    "arrow arrow";

}
.info p {
    margin: 10px 0 0 30px;
    font-size: 30px;
}
.status {
    grid-area: status;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
.current_status {
        background: #6574FF;
        border-radius: 30px;
        padding: 7px 20px;
        margin: 0 30px 0 10px;
        max-width: 250px;
        text-align: center;
        color: #FFFFFF;
}
.status p {
    font-size: 20px;
}
    .job {
    grid-area: job;
    margin: 0 0 20px 30px;
}
.job_text p {
    padding:0 0 5px 0;
    margin: 0;
    color: #6B5581;
    font-style: normal;
}
.task {
    grid-area: task;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-direction: row;
    padding-bottom: 10px;
}
.task p {
    margin: 0 80px 0 30px;
    color: #666666;
    font-style: normal;
    font-weight: normal;
    font-size: 20px;
    white-space: nowrap;
}
.current_task {
    margin: 0 30px 0 0;
    background: #6573FE;
    border-radius: 30px;
    padding: 10px 50px 5px 50px;
    color: #FFFFFF;
    text-align: center;
}
.all_tasks {
    width: 100%;
    display: flex;
    justify-content: space-around;
    align-items: flex-end;
    flex-wrap: wrap;
    margin: 0;
}
.tasks {
    margin: 0 20px 10px 20px;
}
}
</style>
{#await fetch_data()}
    {:then json}
<div class="component" transition:fade="{{duration: 300}}">
    <div class="team">
        {#each json['members'] as member, num}
        <div class="member_box">
        <div class="member">
            <div class="info"><p>{member['user']['name']} {member['user']['surname']}</p></div>
            <div class="status"><p>Статус: </p><div class="current_status">{member['user']['status']}</div></div>
            <div class="job"><div class="job_text"><p>{member['user']['profession']}</p></div></div>
            {#if member['tasks'].length>0}
            <div class="task"><p>Выполняемая задача</p><div class="current_task">{member['tasks'][0]['description']}</div></div>
                {:else}
            <div class="task"><p>Выполняемая задача</p><div class="current_task">задач нет</div></div>
                {/if}
        </div>
            {#if bool_arr[num] === '1' && member['tasks'].length>1}
            <div class="all_tasks" transition:slide|local>
                {#each member as task, ind}
                    {#if ind>0}
                    <div class="tasks">{task['description']}</div>
                    {/if}
                {/each}
                {#if member.length===ind}
                <div class="tasks">Больше нет задач</div>
                    {/if}
            </div>
            {/if}
            <div class="arrow"><img class="arrow_image {member[0] === '1' ? 'transformed_arrow' : ''}" src="/array.svg" alt="" on:click={() => drop(num)}></div>
        </div>
            {/each}
    </div>
</div>
{/await}