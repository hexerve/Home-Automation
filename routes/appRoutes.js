'use strict';
module.exports = function (app) {

    var User = require('../controllers/userController');
    var mosquito = require('../controllers/mosquito');
    var responses = require('../helper/responses');
    var VerifyToken = require('../helper/verifyToken');

    // user Routes
    app.get("/", function (req, res) {
        var message;
        if (req.query.fileErr && req.query.fileErr === "true") {
            message = true;
        } else {
            message = false;
        }
        res.render("login", {
            message: false
        });
    });

    app.get("/dashboard", function (req, res) {
        res.render("dashboard", {
            error: false
        });
    });

    app.get("/devices", function (req, res) {
        res.render("devices");
    });

    app.post("/devices", VerifyToken, User.addDevice);

    app.put("/devices", VerifyToken, User.updateDevice);

    app.delete("/devices", VerifyToken, User.removeDevice);

    app.get("/resetpass", function (req, res) {
        res.render("resetPass");
    });

    app.get("/profile", function (req, res) {
        res.render("profile");
    });

    app.get("/admin", function (req, res) {
        res.render("admin");
    });

    app.post("/login", User.login);

    app.post("/register", User.register);

    app.post("/reverify", User.sendVerificationLink);

    app.put("/password/reset", VerifyToken, User.changePassword);

    app.get("/password/forget", function (req, res) {
        res.render("forgetPass");
    });

    app.put("/password/forget", User.forgetPassword);

    app.get("/password/set", function (req, res) {
        res.render("setPass",{
            message: null
        });
    });

    app.put("/password/set", User.setPassword);

    app.get('/verify/email/:token', VerifyToken, User.verify);
    
    app.get("/user", VerifyToken, User.current_user);

    app.put("/user", VerifyToken, User.updatePersonalInfo);

    app.get("/adminAcesss/user/:email", VerifyToken, User.getUserData);

    app.put("/adminAcesss/user", VerifyToken, User.updateUser);

    app.post('/verify/email', User.sendVerificationLink);


    app.put("/operate", VerifyToken, mosquito.operate);

    // star routes
    app.get('*', function (req, res) {
        res.redirect(301, "../");
    });

    app.put('*', function (req, res) {
        res.redirect(301, "../");
    });

    app.delete('*', function (req, res) {
        res.redirect(301, "../");
    });

    app.post('*', function (req, res) {
        res.redirect(301, "../");
    });

};