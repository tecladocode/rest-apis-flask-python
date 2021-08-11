var fs = require("fs");
var path = require("path");

module.exports = function(...childPaths) {
  var curriculumFolder = path.basename(path.dirname(__dirname));
  var lectureFolder = path.join(curriculumFolder, ...childPaths);
  var files = fs.readdirSync(lectureFolder).sort();
  var outputPaths = [];

  for (var i in files) {
    var finalPath = path.join(lectureFolder, files[i], path.sep);
    if (fs.existsSync(finalPath) && fs.lstatSync(finalPath).isDirectory()) {
      outputPaths.push(path.join(path.sep, ...childPaths, files[i], path.sep).replace(/\\/g, '/'));
    }
  }
  console.log(outputPaths);
  return outputPaths;
};
