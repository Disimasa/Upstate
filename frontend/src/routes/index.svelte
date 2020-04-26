<script>
    import {url} from '../../static/site_url.js';
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
    private_token = localStorage.getItem('cookie_private');
}
    const resp = await fetch(url + 'create/team', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'creator_token':private_token})
    });
    const json = await resp.json();
    alert(json['name']);
}
</script>
<style>
.create_team {
    margin-top: 200px;
}
</style>
<button class="create_team" on:click={Create_team}>Создать команду</button>