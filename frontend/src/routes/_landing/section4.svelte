<style>
    section {
        font-family: Comfortaa, sans-serif;
        width: 100vw;
        height: 70vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: #f8f8f8;
    }

    .text {
        margin-top: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 70vw;
    }

    h1 {
        text-align: center;
        font-size: 2.7em;
    }

    .first {
        text-align: center;
        color: #737373;
    }

    .second {
        text-align: center;
    }
    .platforms {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        margin-top: 4vh;
    }
    .platform_title {
        color: #606060;
        font-size: 1.2em;
        text-align: center;
    }
    .platform_description {
        color: #929292;
        font-size: 1em;
        text-align: center;
    }
    .platforms div {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        max-width: 350px;
    }

    img {
        margin-top: 20px;
        margin-bottom: 20px;
    }

</style>

<section>
    <div class="text">
        <h1>На нас можно положиться</h1>
        <h2 class="first">Доверьте статусы Вашей команды нашей экосистеме сервисов. Обо всем остальном позаботимся мы</h2>
        <h2 class="second">Поддерживаемы платформы:</h2>
    </div>
    <div class="platforms">
        <div class="vk">
            <img src="landing/VK.png">
            <h2 class="platform_title">ВК бот</h2>
            <h2 class="platform_description">
                Меняйте свой статус и смотрите чужой,
                не выходя из соцсети
            </h2>

        </div>
        <div class="alice">
            <img src="landing/Alisa.png">
            <h2 class="platform_title">Алиса</h2>
            <h2 class="platform_description">Получите все перимущества голосого помощника</h2>
        </div>
        <div class="tg">
            <img src="landing/Telegram.png">
            <h2 class="platform_title">Телеграм</h2>
            <h2 class="platform_description">Раскройте всю мощь командного менеджмента</h2>
        </div>
    </div>


</section>