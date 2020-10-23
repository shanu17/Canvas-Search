const express = require("express");
const port = 3000;
const path = require('path');

const app = express();

//Template Manager EJS
app.set("view engine", "ejs");
app.engine("ejs", require("ejs").__express);

//Public facing folder
const publicDirectory = path.join(__dirname, "./public");
app.use(express.static('views'));
app.use(express.static(publicDirectory));

//Enable us to use POST data
app.use(express.urlencoded({extended: false}));
app.use(express.json());

//Define Routes
app.use("/", require("./routes/pages"));

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});