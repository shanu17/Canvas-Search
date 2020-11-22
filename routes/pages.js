const express = require("express");
const request = require("request");
const fs = require('fs');
const fsPromises = fs.promises;
var cors = require('cors');
const axios = require('axios')
const {PythonShell} =require('python-shell'); 

const router = express.Router();

router.get("/", cors(),(req, res) => {
	res.render("index");
});
//|| itemsList[k].title.includes(".pptx")
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
		if (fs.existsSync(userDir)) {
			console.log("already fetched user")
		} else{
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
							if(itemsList[k].title.includes(".pdf")) {
								let fileUrl = itemsList[k].url + "?access_token=" + token;
								response = await axios.get(fileUrl);
								if(response.status !== 200) {
									return res.status(404).send("Error accessing files in Module Items");
								}
								body = response.data;
								let files = body;
								let downloadPath = userDir + "/" + files.filename;
								if(!fs.existsSync(downloadPath)) {
									console.log(downloadPath);
									axios.get(files.url, {responseType: "stream"}).then((response) => {
										response.data.pipe(fs.createWriteStream(downloadPath));
									});
								}
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

router.get("/generate", (req, res) => {
	// console.log("from generate request",req.query.path); 
	console.log("coming in generate");
	let options = { 
		mode: 'text', 
		pythonOptions: ['-u'], // get print results in real-time
		//If you are having python_test.py script in same folder, then it's optional. 
		args: [req.query.path] //An argument which can be accessed in the script using sys.argv[1] 
	}; 
		

    PythonShell.run('index_run.py', options, function (err, result){ 
          if (err) throw err; 
          // result is an array consisting of messages collected  
          //during execution of script. 
          console.log('result: ', result.toString()); 
          res.status(200).send({status:"200"});
    });

});

router.get("/search", (req, res) => {
	let query = req.query.searchQuery;
	let userId = req.query.userId;
	let options = { 
		mode: 'text', 
		pythonOptions: ['-u'], // get print results in real-time
		//If you are having python_test.py script in same folder, then it's optional. 
		args: [userId,query] //An argument which can be accessed in the script using sys.argv[1] 
	}; 
		

    PythonShell.run('query_run.py', options, function (err, result){ 
          if (err) throw err; 
          // result is an array consisting of messages collected  
          //during execution of script. 
          console.log('result: ', result.toString()); 
          res.status(200).send({q: query, result:result.toString()});
    });
	// The userId here will give you which folder to actually use to search for the query
	// Use that and then after that send a JSON object containing the top results
	

});

module.exports = router;