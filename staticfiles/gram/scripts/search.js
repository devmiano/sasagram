function searchDropdown() {
	document.getElementById('searchDropdown').classList.toggle('show');
}
window.onclick = function (e) {
	if (!e.target.matches('.searchbtn, .searchicon')) {
		var myDropdown = document.getElementById('searchDropdown');
		if (myDropdown.classList.contains('show')) {
			myDropdown.classList.remove('show');
		}
	}
};
