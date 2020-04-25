<script>
import { fade } from 'svelte/transition';
let team = '2D-team';
let members = [['Иван', 'Иванов', 'Разработчик', 'Ботаю', 'Покушать'],['Петр', 'Петров', 'Дизайнер', 'Чилю', 'Лечь спать'], ['Анна', 'Аановна', 'Аналитик', 'Сплю', 'Проснуться']]
</script>
<style>
@media all and (min-width: 780px) {


.component {
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
.member {
    width: 600px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 2fr 1fr 2fr;
    grid-template-areas:
    "info status"
    "job status"
    "task task";
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
.info p {
    margin: 20px 0 0 30px;
    font-size: 20px;
}
.status {
    grid-area: status;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
.status p {
    font-size: 20px;
}
.current_status {
    background: #6574FF;
    border-radius: 30px;
    padding: 10px 50px;
    margin: 0 30px 0 20px;
    flex: 1;
    max-width: 150px;
    text-align: center;
    color: #FFFFFF;
}
.job {
    grid-area: job;
    margin: 0 0 0 30px;
}
.job_text {
    display: inline-block;
    border-bottom: 2px solid #939DFF;
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
    padding-bottom: 20px;
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
    padding: 10px 50px;
    color: #FFFFFF;
    text-align: center;
    flex:1;
}
}
</style>
<div class="component" transition:fade="{{duration: 500}}">
    <div class="team">
        {#each members as member}
        <div class="member">
            <div class="info"><p>{member[0]} {member[1]}</p></div>
            <div class="status"><p>Статус: </p><div class="current_status">{member[3]}</div></div>
            <div class="job"><div class="job_text"><p>{member[2]}</p></div></div>
            <div class="task"><p>Выполняемая задача</p><div class="current_task">{member[4]}</div></div>
        </div>
            {/each}
    </div>
</div>