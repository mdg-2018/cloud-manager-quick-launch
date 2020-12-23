const client = stitch.Stitch.initializeDefaultAppClient("mside-rqcve");

if (client.auth.hasRedirectResult()) {
    client.auth.handleRedirectResult().then(user => {
        console.log(user);
    });
}

var errCt = 0;

window.login = async function(){
    try {
        if (!client.auth.isLoggedIn) {
            const credential = new stitch.GoogleRedirectCredential(window.location.origin);
            client.auth.loginWithRedirect(credential);
        } else {
            console.log(client.auth.currentUser);
        }
    }
    catch(e) {
        errCt++;
        console.log("try " + errCt);
        console.log(e);
        if(errCt < 5) {
            setTimeout(function() { login();}, 500);
        }
    }
}

window.getCurrentUserName = async function() {
    return client.auth.currentUser.profile.name||"";
}

window.getCurrentUserIcon = async function() {
    return client.auth.currentUser.profile.pictureUrl||"/user.png";
}

window.getCurrentUser = async function() {
    return client.auth.currentUser.id;
}

window.getCurrentUserEmail = async function() {
    return (client.auth.currentUser.profile.email.replace("@","").replace(/\./g,"")||"UNKNOWNUNKNOWNUNKNOWN");
}