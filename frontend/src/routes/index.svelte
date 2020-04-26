<script>
    import Component1 from './_landing/section1.svelte';
    import Component2 from './_landing/section2.svelte';
    import Component3 from './_landing/section3.svelte';
    import Component4 from './_landing/section4.svelte';
    import Component5 from './_landing/section5.svelte';
    import {url} from '../../static/site_url.js';
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
.create_team {
    margin-top: 200px;
}
</style>
<Component1/>
<Component2/>
<Component3/>
<Component4/>
<Component5/>