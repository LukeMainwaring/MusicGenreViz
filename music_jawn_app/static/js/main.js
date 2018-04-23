console.log("js")
var slider = document.getElementById("myRange");
//var output = document.getElementById("demo");
//output.innerHTML = slider.value; // Display the default slider value
$(".demo").text(slider.value)
console.log(slider.value)

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    //output.innerHTML = this.value;
    $(".demo").text(slider.value)
    console.log(slider.value)
}