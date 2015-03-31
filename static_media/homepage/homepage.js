$("#category-submit").on("click", function(){
    $("#images-container").html('');
    var category_text = document.getElementById("category-text").value;
    if(category_text === ""){
        $("error-status").show();
        $("#error-status").html("Please give a category.");
        return 0;
    }
    var data = {
        "category": category_text,
    };
    var images_url = "/core/fetch_images/"+category_text+"/"; 
    $("error-status").show();
    $("#error-status").html("Loading may take some time. Please wait");
    $.ajax({
        url: images_url,
        type: "GET",
        success: function(response){
            if(response["status"]==="OK"){
                $("#images-container").append(response["html_text"]);
                $("#error-status").hide();
                $("#job-id").append(response["job_id"]);
            }
        }
    });
});
$("#train-model").on("click", function(){
    var job_id = $("#job-id").text();
    var no_images = $("#images-container").children().length;
    if(job_id === "" || no_images == 0){
        $("error-status").show();
        $("error-status").html("Category not given or Images not found for training model.");            
    }
    data = {
        "job_id": job_id, 
    };
    $.ajax({
        url: "/utility/train_model/",
        type: "POST",
        data: data,
        success: function(response){
            $("error-status").show();
            if(response["status"]=="OK"){
                $("#error-status").html("Model Successfully Trained");
            }
            else{
                $("#error-status").html(response["html_status"]);
            }
        }
    });
});
