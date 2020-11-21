const express = require("express");
const request = require("request");
const fs = require('fs');
const fsPromises = fs.promises;
var cors = require('cors');
const axios = require('axios')

const router = express.Router();

router.get("/", cors(),(req, res) => {
	res.render("index");
});

router.post("/search", cors(), async (req, res) => {
	const {token} = req.body;
	var userDir;
	if (!token) {
		return res.redirect("/");
	}

	let url = "https://canvas.pitt.edu/api/v1/users/self/profile?access_token=" + token;
	try {
		let response = await axios.get(url)
		if (response.status !== 200) {
			return res.status(404).send("Error Invalid Canvas user");
		}

		let body = response.data
		let userProfile = body;
		userDir = "./" + userProfile.id;
		if(!fs.existsSync(userDir))
			fs.mkdirSync(userDir);
		let courseUrl = "https://canvas.pitt.edu/api/v1/users/self/courses?access_token=" + token;
		response = await axios.get(courseUrl);
		if(response.status !== 200) {
			return res.status(404).send("Error cannot retrieve Courses for User ID" + userProfile.id);
		}
		body = response.data;
		let courseList = body;
		for(let i in courseList) {
			let moduleUrl = "https://canvas.pitt.edu/api/v1/courses/" + courseList[i].id + "/modules?access_token=" + token + "&per_page=20	";
			response = await axios.get(moduleUrl);
			if(response.status !== 200) {
				return res.status(404).send("Error cannot retrieve Modules for Course " + courseList[i].name);
			}
			body = response.data;
			let moduleList = body;
			if(moduleList.length > 0) {
				for(let j in moduleList) {
					let itemsUrl = moduleList[j].items_url + "?access_token=" + token;
					let response = await axios.get(itemsUrl);
					if(response.status !== 200) {
						return res.status(404).send("Error cannot retrieve Modules items for Course ");
					}
					body = response.data;
					let itemsList = body;
					for(let k in itemsList) {
						if(itemsList[k].title.includes(".pdf") || itemsList[k].title.includes(".ppt")) {
							let fileUrl = itemsList[k].url + "?access_token=" + token;
							response = await axios.get(fileUrl);
							if(response.status !== 200) {
								return res.status(404).send("Error accessing files in Module Items");
							}
							body = response.data;
							let files = body;
							let downloadPath = userDir + "/" + files.filename;
							if(!fs.existsSync(downloadPath)) {
								let fileContents = axios.get(files.url);
								await fsPromises.writeFile(downloadPath, fileContents);
							}
						}
					}
				}
			}
		}
		res.render("search", {user: userProfile.id});
	}
	catch (error) {
		return res.status(404).send("Error accessing Canvas user");
	}
});

router.get("/search", (req, res) => {
	let query = req.query.searchQuery;
	let userId = req.query.userId;
	// The userId here will give you which folder to actually use to search for the query
	// Use that and then after that send a JSON object containing the top results
	res.status(200).send({q: query});
});

module.exports = router;