<script>
    import {url} from '../../../static/site_url.js';
    let team_token;
    let public_token;
    let private_token;
async function Create_team() {
    localStorage.removeItem('public_token');
    public_token = localStorage.getItem('public_token');
if (public_token === null) {
    const resp = await fetch(url + 'create/user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'platform_id': document.documentElement.clientWidth+' '+document.documentElement.clientHeight,
        'platform_name':'web', 'name':'', 'surname':''})
    });
    const json = await resp.json();
    alert(json['user']['name']);
    public_token = json['user']['public_token'];
    private_token = json['user']['private_token'];
    localStorage.setItem('public_token', public_token);
    localStorage.setItem('private_token', private_token);
} else {
    private_token = localStorage.getItem('private_token');
}
    const resp = await fetch(url + 'create/team', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'creator_token':private_token})
    });
    const json = await resp.json();
    team_token = json['public_token'];
    localStorage.setItem('team_token', team_token);
    alert(json['name']);
}
</script>
<style>
    section {
        font-family: Comfortaa, sans-serif;
        width: 100vw;
        height: 70vh;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        background-color: #f8f8f8;
    }

    h1 {
        font-size: 2.5em;
        color: #4F4F4F;
    }

    h2 {
        color: #737373;
        font-size: 1.4em;
    }

    .text {
        display: flex;
        flex-direction: column;
        height: 100%;
        margin-right: 40px;
    }

    img {
        width: 45vw;
        height: 45vw;
        max-height: 400px;
        max-width: 320px;
    }
    .section-container {
        width: 70vw;
        display: flex;
        flex-direction: row;
        align-items: center;
    }
    button {
        margin-top: 40px;
        appearance: none;
        background-color: #636DFF;
        color: white;
        font-family: 'Comfortaa', sans-serif;
        border: 1px solid transparent;
        border-radius: 60px;
        padding: 0.8em;
        min-width: 200px;
        max-width: 400px;
        box-shadow: 5px 4px 26px 1px #908DFF;
        transition: 1s ease;
    }
    button:hover {
        background-color: #727AFF;
        box-shadow: 5px 4px 26px 4px #908DFF;
    }
    .JoinNow {
        font-size: 1.5em;
    }
    .NoReg {
        font-size: 0.8em;
    }

</style>

<section>
    <div class="section-container">
        <div class="text">
            <h1>Доступный веб-интерфейс</h1>
            <h2>Мы адаптировали дизайн основного сервиса для того чтобы Вы смогли раскрыть весь потенциал платформы без
                привязки к определенному устройству</h2>
            <button on:click={Create_team}>
                <span class="JoinNow">Присоединиться сейчас</span><br>
                <span class="NoReg">Регистрация не требуется!</span>
            </button>
        </div>
        <div><img alt="mockup" src="landing/mockup.png"></div>
    </div>
</section>