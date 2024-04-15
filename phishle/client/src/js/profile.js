$(function(){
    $("#profileDetails").click(function(){
        
    });
    $("#signUp").click(function(){
        window.location.href = "login.html";
    });

    $("#profileDetails").attr('disabled', true);
    

    $("#leaderboard").DataTable({
        responsive:true
    });
    
});

