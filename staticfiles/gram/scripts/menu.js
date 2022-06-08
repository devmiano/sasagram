function menuDropdown() {
	document.getElementById('menuDropdown').classList.toggle('show');
}
window.onclick = function (e) {
	if (!e.target.matches('.dropbtn, .dropphoto')) {
		var myDropdown = document.getElementById('menuDropdown');
		if (myDropdown.classList.contains('show')) {
			myDropdown.classList.remove('show');
		}
	}
};
