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
<section>
    <div class="image"><img alt="leaves" src="landing/leaves.png"></div>
    <div class="container">
        <h1>Upstate</h1>
        <h2>Твой статус в будущем, которое уже наступило</h2>
        <button on:click={Create_team}>Поменять статус</button>
    </div>
</section>

<style>
    section {
        z-index: 20;
        margin-top: 70px;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        border-top-left-radius: 90px;
        border-top-right-radius: 90px;
        background-color: #F8F8F8;
        height: 100vh;
    }

    h1 {
        font-family: Roboto, sans-serif;
        font-size: 9em;
        border-bottom: 12px solid #2FFF9B;
        color: #4B4B4B;
    }

    h2 {
        font-family: Roboto, sans-serif;
        font-size: 2.5em;
        color: #4B4B4B;
        text-align: right;
        margin-top: -30px;
    }

    .image {
        width: 40vw;
        margin-left: 10vw;
    }
    img {
        margin-top: 100px;
        width: 100%;
        max-width: 400px;
        min-width: 200px;
    }

    .container {
        margin-right: 10vw;
        margin-top: 140px;
        display: flex;
        flex-direction: column;
        width: 60vw;
        align-items: flex-end;
    }

    button {
        margin-top: 40px;
        appearance: none;
        background-color: #636DFF;
        color: white;
        font-size: 2em;
        font-family: 'Comfortaa', sans-serif;
        border: 1px solid transparent;
        border-radius: 60px;
        padding: 0.8em;
        min-width: 500px;
        box-shadow: 5px 4px 26px 1px #908DFF;
        transition: 1s ease;
    }
    button:hover {
        background-color: #727AFF;
        box-shadow: 5px 4px 26px 4px #908DFF;
    }
</style>