<!--<nav>-->
<!--	<ul>-->
<!--		<li><a aria-current='{segment === undefined ? "page" : undefined}' href='.'>home</a></li>-->
<!--		<li><a aria-current='{segment === "about" ? "page" : undefined}' href='about'>about</a></li>-->

<!--		&lt;!&ndash; for the blog link, we're using rel=prefetch so that Sapper prefetches-->
<!--		     the blog data when we hover over the link or tap it on a touchscreen &ndash;&gt;-->
<!--		<li><a rel=prefetch aria-current='{segment === "blog" ? "page" : undefined}' href='blog'>blog</a></li>-->
<!--	</ul>-->
<!--</nav>-->

<script>
	export let segment;
</script>
<link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;500&display=swap" rel="stylesheet">

<style>
@media all and (max-width: 780px) {
	.header {
		position:absolute;
		top:0;
		right: 27px;
		width: 45px;
		height: 400px;
		display: flex;
		flex-direction: column;
		z-index: 10;
	}
	.main, .personal, .team {
		width: 100px;
		height: 44px;
		background-color: #ffffff;
		display: flex;
		justify-content: center;
		align-items: center;
		font-family: 'Comfortaa', cursive;
		font-style: normal;
		font-weight: normal;
		font-size: 15px;
		border-radius: 0 0 20px 20px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
		-webkit-transform: rotate(90deg);
		transform: rotate(90deg);
		margin: 40px 0 30px 0;
		color: #666666
	}
	.main, .personal, .team:hover {
		cursor: pointer;
	}
	.active {
		background-color: #6574FF;
		color: #ffffff;
	}
}
@media all and (min-width: 780px) {
	.header {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 70px;
		background-color: #E5E5E5;
		display: grid;
		grid-template-columns: 20% minmax(50px, 50%) minmax(130px, 12%) minmax(130px, 12%) minmax(130px, 12%) 20px;
		grid-template-areas: "logo . main personal team .";
		gap: 30px;
		margin: 0;
		padding: 0;
	}

	.logo {
		grid-area: logo;
	}

	.main, .personal, .team {
		height: 40px;
		background-color: #ffffff;
		display: flex;
		justify-content: center;
		align-items: center;
		font-family: 'Comfortaa', cursive;
		border-radius: 0 0 20px 20px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
	}

	.main, .personal, .team:hover {
		cursor: pointer;
	}

	.main {
		grid-area: main;
	}

	.personal {
		grid-area: personal;
	}

	.team {
		grid-area: team;
	}

	.active {
		background-color: #6574FF;
		color: #ffffff;
	}
}
</style>

<header class="header">
	<a class="logo"></a>
	<a class="main {segment === undefined ? 'active':''}" href=".">Главная</a>
	<a class="personal {segment === 'profile' ? 'active':''}" href="profile">Профиль</a>
	<a class="team {segment === 'team' ? 'active':''}" href="team">Команда</a>
</header>

<!--<nav>-->
<!--	<ul>-->
<!--		<li><a aria-current='{segment === undefined ? "page" : undefined}' href='.'>home</a></li>-->
<!--		<li><a aria-current='{segment === "about" ? "page" : undefined}' href='about'>about</a></li>-->

<!--		&lt;!&ndash; for the blog link, we're using rel=prefetch so that Sapper prefetches-->
<!--		     the blog data when we hover over the link or tap it on a touchscreen &ndash;&gt;-->
<!--		<li><a rel=prefetch aria-current='{segment === "blog" ? "page" : undefined}' href='blog'>blog</a></li>-->
<!--	</ul>-->
<!--</nav>-->