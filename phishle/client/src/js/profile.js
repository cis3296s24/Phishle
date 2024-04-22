$(function(){
    var req  = $.ajax({url:"http://localhost:5000/getGlobalLeaderboard", method:"GET", success: function(data){
        var tableString = "";
        $.each(data, function(index, value){
            var pos = index+1
            tableString += "<tr><th>"+pos+"</th><td>"+value[0]+"</td><td>"+value[1]+"</td><td>"+value[2]+"</td></tr>"
        });
        $("#globalLeaderboard").append(tableString)
        
    }})
    req.done(function(msg){
        $("#leaderboard").DataTable({
            responsive:true
        });
    })


    $("#profileDetails").click(function(){
        
    });
    $("#signUp").click(function(){
        window.location.href = "login.html";
    });

    $("#profileDetails").attr('disabled', true);
    
    
});

