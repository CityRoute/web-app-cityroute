// script to automate the creation of jest files

var fs = require("fs");
var components = fs.readdirSync("../src/components/");
// var views = fs.readdirSync("../src/views/");

fs.readFile("../tests/unit/template.js", "utf8", (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  console.log(data);
  components.forEach(function(file) {
    let name = file
      .split(".")
      .slice(0, -1)
      .join(".");

    let lower_name = name.toLowerCase();
    copyFile(lower_name);
    fs.readFile(
      "../tests/unit/components/" + lower_name + ".spec.js",
      "utf8",
      function(err, data) {
        if (err) {
          return console.log(err);
        }
        var result = data.replace(/template_name/g, name);

        fs.writeFile(
          "../tests/unit/components/" + name + ".spec.js",
          result,
          "utf8",
          function(err) {
            if (err) return console.log(err);
          }
        );
      }
    );
    console.log(name);
  });
});

async function copyFile(name) {
  await fs.copyFile(
    "../tests/unit/template.js",
    "../tests/unit/components/" + name + ".spec.js",
    (err) => {
      if (err) throw err;
      console.log("source.txt was copied to destination.txt");
    }
  );
}
