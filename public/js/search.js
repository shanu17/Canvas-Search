var userId;
const searchForm = document.getElementById("searchForm");

window.addEventListener("load", (e) => {
	userId = document.getElementById("userId").innerText.trim();
	console.log(searchForm.style.display)
	searchForm.style.visibility= "hidden";
	// searchForm.style.display = "none";
	var req2;
	req2 = new XMLHttpRequest();
	req2.responseType = "json";
	let url = "http://localhost:3000/generate?path="+userId;
	req2.open("GET", url, true);
	req2.send();

	req2.onreadystatechange = function() {
		if(this.readyState == 4 && this.status == 200) {
			console.log("synchronous");
			searchForm.style.visibility= "initial";
		}
	}
});

searchForm.addEventListener("submit", (e) => {
	e.preventDefault();
	let q = document.getElementById("searchQuery").value;
	var req;
	req = new XMLHttpRequest();
	req.responseType = "json";

	let url = "http://localhost:3000/search?searchQuery=" + q + "&userId=" + userId;
	req.open("GET", url, true);
	req.send();
	userId = document.getElementById("userId").innerText.trim();
	req.onreadystatechange = function() {
		if(this.readyState == 4 && this.status == 200) {
			// console.log(this.response.q);
			// console.log("hello")
			// console.log(this.response.result)
			division = document.getElementById("results_display");
			division.innerHTML=""
			for  (var x in this.response.result) {
				division.innerHTML += "<a href=\""+userId+"/"+this.response.result[x].docname+"\">"+this.response.result[x].docname+"</a>"
				// console.log(this.response.result[x].docname)
			}
			searchForm.reset();
			// division = document.getElementById("results_display");

			
		}
	}
});