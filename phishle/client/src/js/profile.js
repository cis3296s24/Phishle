$(function(){
    var user = sessionStorage.getItem("username");
    var usergroup = 0
    if(user){
        var profileUrl = "http://localhost:5000/getProfileInfo/" + user
        var prof = $.ajax({url:profileUrl, method:"GET", success: function(data){
            $("#username").html(data.username);
            $("#streak").html(data.currentstreak + " days")
            $("#currentStreak").html(data.currentstreak + " days")
            $("#highStreak").html(data.longeststreak + " days")
            $("#cardusername").html(data.username);
            usergroup = data.group_id
            if(usergroup != 0){
                var grpurl = "http://localhost:5000/getGroupLeaderboard/" + usergroup
                var grpReq = $.ajax({url:grpurl, method:"GET", success: function(data){
                    var tableString = "";
                    $.each(data, function(index, value){
                        var pos = index+1
                        if(value[0] === user){
                            $("#groupRanking").html(pos);
                        }
                        tableString += "<tr><th>"+pos+"</th><td>"+value[0]+"</td><td>"+value[1]+"</td><td>"+value[2]+"</td></tr>"
                    });
                
                
                    $("#groupLeaderboardBody").append(tableString)
                }});
                grpReq.done(function(msg){
                    $("#groupLeaderboard").DataTable({
                        responsive:true
                    });
                })
            }else{
                console.log(usergroup)
                $("#groupLeaderboardBody").append("You are not in a group! Add yourself to a group to see the group leaderboard.")
            }
        }});
    }
    else{
        $("#notsignedin").show();
        $("#signUp").show();
        $("#profileDetails").attr('disabled', true);
        $("#userCard").hide();
    }

    var req  = $.ajax({url:"http://localhost:5000/getGlobalLeaderboard", method:"GET", success: function(data){
        var tableString = "";
        $.each(data, function(index, value){
            var pos = index+1
            if(value[0] === user){
                $("#globalRanking").html(pos);
            }
            tableString += "<tr><th>"+pos+"</th><td>"+value[0]+"</td><td>"+value[1]+"</td><td>"+value[2]+"</td></tr>"
        });
        $("#globalLeaderboardBody").append(tableString)
        
    }});
    req.done(function(msg){
        $("#globalLeaderboard").DataTable({
            responsive:true
        });
    })


    

    
    

    $("#profileDetails").click(function(){
        
    });
    $("#signUp").click(function(){
        window.location.href = "login.html";
    });

    
    
});

