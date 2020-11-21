var userId;
const searchForm = document.getElementById("searchForm");
window.addEventListener("load", (e) => {
	userId = document.getElementById("userId").innerText.trim();
});

searchForm.addEventListener("submit", (e) => {
	e.preventDefault();
	let q = document.getElementById("searchQuery").value;
	var req;
	req = new XMLHttpRequest();
	req.responseType = "json";
	req.onreadystatechange = function() {
		if(this.readyState == 4 && this.status == 200) {
			console.log(this.response.q);
		}
	}
	let url = "http://localhost:3000/search?searchQuery=" + q + "&userId=" + userId;
	req.open("GET", url, true);
	req.send();
});