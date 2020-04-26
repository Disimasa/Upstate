<script>
    import {url} from '../../../static/site_url.js';
    import { onMount } from 'svelte';
    let dir;
    let public_token;
    let private_token;
    let team_token;
    onMount(fetch_data);
    async function fetch_data() {
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
        dir = window.location.href;
        let teams_token = dir.split('/');
        team_token = teams_token[teams_token.length-1];
        const resp = await fetch(url + 'enter/team', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'team_token': team_token, 'user_token': private_token})
    });
        localStorage.setItem('team_token', team_token);
    const json = await resp.json();
    }
</script>