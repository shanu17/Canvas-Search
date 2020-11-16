const express = require("express");
const request = require("request");
const fs = require('fs');

const router = express.Router();

router.get("/", (req, res) => {
	res.render("index");
});

router.post("/search", (req, res) => {
	const {token} = req.body;
	if (token) {
		let url = "https://canvas.pitt.edu/api/v1/users/self/profile?access_token=" + token;
		request.get(url, { json: true }, (error, response, body) => {
			console.log(response);
			if(error)
				return res.status(404).send("Error accessing Canvas user");
			if(response.statusCode == 200) {
				let userProfile = body;
				let userDir = "./" + userProfile.id;
				if(!fs.existsSync(userDir))
					fs.mkdirSync(userDir);
				let courseUrl = "https://canvas.pitt.edu/api/v1/users/self/courses?access_token=" + token;
				request.get(courseUrl, {json: true}, (error, response, body) => {
					if(error)
						return res.status(404).send("Error accessing Courses for Canvas User ID" + userProfile.id);
					if(response.statusCode == 200) {
						let courseList = body;
						for(let i in courseList) {
							let moduleUrl = "https://canvas.pitt.edu/api/v1/courses/" + courseList[i].id + "/modules?access_token=" + token + "&per_page=20	";
							request.get(moduleUrl, {json: true}, (error, response, body) => {
								if(error)
									return res.status(404).send("Error accessing modules of Course " + courseList[i].name);
								if(response.statusCode = 200) {
									let moduleList = body;
									if(moduleList.length > 0) {
										for(let j in moduleList) {
											let itemsUrl = moduleList[j].items_url + "?access_token=" + token;
											request.get(itemsUrl, {json: true}, (error, response, body) => {
												if(error)
													return res.status(404).send("Error accessing Module Items");
												let itemsList = body;
												for(let k in itemsList) {
													if(itemsList[k].title.includes(".pdf") || itemsList[k].title.includes(".ppt")) {
														let fileUrl = itemsList[k].url + "?access_token=" + token;
														request.get(fileUrl, {json: true}, (error, response, body) => {
															if(error)
																return res.status(404).send("Error accessing files in Module Items");
															let files = body;
															
														});
													}
												}
											});
										}
									}
								} else
								return res.status(404).send("Error cannot retrieve Modules for Course " + courseList[i].name);
							});
						}
						return res.render("search");
					} else {
						return res.status(404).send("Error cannot retrieve Courses for User ID" + userProfile.id);
					}
				});
			} else {
				return res.status(404).send("Error Invalid Canvas user");
			}
		});
	} else {
		res.render("/");
	}
});
module.exports = router;