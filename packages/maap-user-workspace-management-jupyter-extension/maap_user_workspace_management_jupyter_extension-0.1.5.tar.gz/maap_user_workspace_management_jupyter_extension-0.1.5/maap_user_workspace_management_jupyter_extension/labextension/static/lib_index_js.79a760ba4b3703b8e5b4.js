"use strict";
(self["webpackChunkmaap_user_workspace_management_jupyter_extension"] = self["webpackChunkmaap_user_workspace_management_jupyter_extension"] || []).push([["lib_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/*
    See the JupyterLab Developer Guide for useful CSS Patterns:

    https://jupyterlab.readthedocs.io/en/stable/developer/css.html
*/
.Toastify__toast-body {
    overflow: auto;
  }`, "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA;;;;CAIC;AACD;IACI,cAAc;EAChB","sourcesContent":["/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n.Toastify__toast-body {\n    overflow: auto;\n  }"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!***************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \***************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, `
`, "",{"version":3,"sources":[],"names":[],"mappings":"","sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./lib/dialogs.js":
/*!************************!*\
  !*** ./lib/dialogs.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DialogEnter: () => (/* binding */ DialogEnter),
/* harmony export */   isEmpty: () => (/* binding */ isEmpty),
/* harmony export */   popup: () => (/* binding */ popup),
/* harmony export */   popupResult: () => (/* binding */ popupResult),
/* harmony export */   popupTitle: () => (/* binding */ popupTitle),
/* harmony export */   showDialogEnter: () => (/* binding */ showDialogEnter)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);

const notImplemented = [];
class DialogEnter extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog {
    /**
     * Create a dialog panel instance.
     *
     * @param options - The dialog setup options.
     */
    constructor(options = {}) {
        super(options);
    }
    handleEvent(event) {
        switch (event.type) {
            case 'keydown':
                this._evtKeydown(event);
                break;
            case 'click':
                this._evtClick(event);
                break;
            case 'focus':
                this._evtFocus(event);
                break;
            case 'contextmenu':
                event.preventDefault();
                event.stopPropagation();
                break;
            default:
                break;
        }
    }
    _evtKeydown(event) {
        // Check for escape key
        switch (event.keyCode) {
            case 13: // Enter.
                //event.stopPropagation();
                //event.preventDefault();
                //this.resolve();
                break;
            default:
                super._evtKeydown(event);
                break;
        }
    }
}
function showDialogEnter(options = {}) {
    let dialog = new DialogEnter(options);
    dialog.launch();
    // setTimeout(function(){console.log('go away'); dialog.resolve(0);}, 3000);
    return;
}
function popup(b) {
    if (!(notImplemented.includes(b.req))) {
        popupTitle(b, b.popupTitle);
    }
    else {
        console.log("not implemented yet");
        popupResult("Not Implemented yet", "Not Implemented yet");
    }
}
function popupTitle(b, popupTitle) {
    showDialogEnter({
        title: popupTitle,
        body: b,
        focusNodeSelector: 'input',
        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Ok' }), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({ label: 'Cancel' })]
    });
}
function popupResult(b, popupTitle) {
    showDialogEnter({
        title: popupTitle,
        body: b,
        focusNodeSelector: 'input',
        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Ok' })]
    });
}
function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}


/***/ }),

/***/ "./lib/funcs.js":
/*!**********************!*\
  !*** ./lib/funcs.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   activateGetPresignedUrl: () => (/* binding */ activateGetPresignedUrl),
/* harmony export */   checkSSH: () => (/* binding */ checkSSH),
/* harmony export */   checkUserInfo: () => (/* binding */ checkUserInfo),
/* harmony export */   getPresignedUrl: () => (/* binding */ getPresignedUrl),
/* harmony export */   getUsernameToken: () => (/* binding */ getUsernameToken)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _getKeycloak__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./getKeycloak */ "./lib/getKeycloak.js");
/* harmony import */ var _widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widgets */ "./lib/widgets.js");
/* harmony import */ var _selector__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./selector */ "./lib/selector.js");
/* harmony import */ var _dialogs__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./dialogs */ "./lib/dialogs.js");
/* harmony import */ var _request__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./request */ "./lib/request.js");







const profileId = 'maapsec-extension:IMaapProfile';
async function checkSSH() {
    (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
        title: 'SSH Info:',
        body: new _widgets__WEBPACK_IMPORTED_MODULE_2__.SshWidget(),
        focusNodeSelector: 'input',
        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'Ok' })]
    });
}
function checkUserInfo() {
    (0,_getKeycloak__WEBPACK_IMPORTED_MODULE_3__.getUserInfo)(function (profile) {
        if (profile['cas:username'] === undefined) {
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.error("Get user profile failed.");
            return;
        }
        let username = profile['cas:username'];
        let email = profile['cas:email'];
        let org = profile['organization'];
        // popup info
        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: 'User Information:',
            body: new _widgets__WEBPACK_IMPORTED_MODULE_2__.UserInfoWidget(username, email, org),
            focusNodeSelector: 'input',
            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'Ok' })]
        });
    });
}
async function getPresignedUrl(state, key, duration) {
    const profile = await getUsernameToken(state);
    return new Promise(async (resolve, reject) => {
        let presignedUrl = '';
        console.log("The key is: ", key);
        var relUrl = "/" + window.location.pathname.split("/")[1] + "/" + window.location.pathname.split("/")[2] + "/jupyter-server-extension/uwm/getSignedS3Url";
        relUrl += "?home_path=" + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption("serverRoot");
        relUrl += "&key=" + key["path"];
        relUrl += "&username=" + profile.uname;
        relUrl += "&proxy-ticket=" + profile.ticket;
        relUrl += "&duration=" + duration;
        (0,_request__WEBPACK_IMPORTED_MODULE_4__.request)('get', relUrl).then((res) => {
            if (res.ok) {
                let data = JSON.parse(res.data);
                console.log(data);
                if (data.status_code == 200) {
                    presignedUrl = data.url;
                    resolve(presignedUrl);
                }
                else if (data.status_code == 404) {
                    resolve(data.message);
                }
                else {
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.error('Failed to get presigned s3 url', { autoClose: 3000 });
                    resolve(data.url);
                }
            }
            else {
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.error('Failed to get presigned s3 url', { autoClose: 3000 });
                resolve(presignedUrl);
            }
        });
    });
}
function activateGetPresignedUrl(app, palette, factory, state) {
    const { commands } = app;
    const { tracker } = factory;
    // matches all filebrowser items
    const selectorItem = '.jp-DirListing-item[data-isdir]';
    const open_command = 'sshinfo:s3url';
    commands.addCommand(open_command, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (!widget) {
                return;
            }
            const item = widget.selectedItems().next();
            if (!item) {
                return;
            }
            let path = item.value;
            let expirationOptions = ['86400 (24 hours)', '604800 (1 week)', '2592000 (30 days)'];
            let dropdownSelector = new _selector__WEBPACK_IMPORTED_MODULE_5__.DropdownSelector(expirationOptions, '86400 (24 hours)', state, path);
            (0,_dialogs__WEBPACK_IMPORTED_MODULE_6__.popupResult)(dropdownSelector, 'Select an Expiration Duration');
        },
        isVisible: () => !!(tracker.currentWidget && tracker.currentWidget.selectedItems().next !== undefined),
        iconClass: 'jp-MaterialIcon jp-LinkIcon',
        label: 'Get Presigned S3 Url'
    });
    app.contextMenu.addItem({
        command: open_command,
        selector: selectorItem,
        rank: 11
    });
    // not adding to palette, since nothing to provide path
    // if (palette) {
    //   palette.addItem({command:open_command, category: 'User'});
    // }
}
let ade_server = '';
var valuesUrl = new URL(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getBaseUrl() + 'jupyter-server-extension/getConfig');
(0,_request__WEBPACK_IMPORTED_MODULE_4__.request)('get', valuesUrl.href).then((res) => {
    if (res.ok) {
        let environment = JSON.parse(res.data);
        ade_server = environment['ade_server'];
    }
});
async function getUsernameToken(state) {
    let defResult = { uname: 'anonymous', ticket: '' };
    if ("https://" + ade_server === document.location.origin) {
        let kcProfile = await (0,_getKeycloak__WEBPACK_IMPORTED_MODULE_3__.getUserInfoAsyncWrapper)();
        if (kcProfile['cas:username'] === undefined) {
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.error("Get profile failed.");
            return defResult;
        }
        else {
            return { uname: kcProfile['cas:username'], ticket: kcProfile['proxyGrantingTicket'] };
        }
    }
    else {
        return state.fetch(profileId).then((profile) => {
            let profileObj = JSON.parse(JSON.stringify(profile));
            return { uname: profileObj.preferred_username, ticket: profileObj.proxyGrantingTicket };
        }).catch((error) => {
            return defResult;
        });
    }
}


/***/ }),

/***/ "./lib/getKeycloak.js":
/*!****************************!*\
  !*** ./lib/getKeycloak.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getToken: () => (/* binding */ getToken),
/* harmony export */   getUserInfo: () => (/* binding */ getUserInfo),
/* harmony export */   getUserInfoAsyncWrapper: () => (/* binding */ getUserInfoAsyncWrapper),
/* harmony export */   updateKeycloakToken: () => (/* binding */ updateKeycloakToken)
/* harmony export */ });
/*
* Race condition was causing error, so if loadUserInfo fails, make sure that keycloak token is updated
*/
var getUserInfo = function (callback, firstTry = true) {
    window.parent._keycloak.loadUserInfo().success(function (profile) {
        callback(profile);
    }).error(async function (err) {
        if (firstTry) {
            console.log('Failed to load profile, trying to update token before retrying', err);
            await updateKeycloakToken(300); // try to update token
            // tested that callback function propagates back to initiator with profile
            getUserInfo(callback, false);
        }
        else {
            console.log('Failed to load profile.', err);
            callback("error");
        }
    });
};
function waitTwoSeconds() {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve();
        }, 2000); // 2000 milliseconds = 2 seconds
    });
}
async function getUserInfoAsyncWrapper() {
    return new Promise((resolve) => {
        getUserInfo((callback) => {
            resolve(callback);
        });
    });
}
var getToken = function () {
    return window.parent._keycloak.idToken;
};
var updateKeycloakToken = async function (seconds, retries = 20) {
    try {
        return await window.parent._keycloak.updateToken(seconds);
    }
    catch (error) {
        if (retries > 0) {
            await waitTwoSeconds();
            await updateKeycloakToken(seconds, retries - 1);
        }
    }
};


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _funcs__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./funcs */ "./lib/funcs.js");
/* harmony import */ var _widgets__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./widgets */ "./lib/widgets.js");
/* harmony import */ var _getKeycloak__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./getKeycloak */ "./lib/getKeycloak.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");








///////////////////////////////////////////////////////////////
//
// Display/inject ssh info extension
//
///////////////////////////////////////////////////////////////
const extensionSsh = {
    id: 'display_ssh_info',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette],
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.ILauncher],
    activate: activateSSH
};
function activateSSH(app, palette) {
    new _widgets__WEBPACK_IMPORTED_MODULE_5__.InjectSSH();
    // Add an application command
    const open_command = 'sshinfo:open';
    app.commands.addCommand(open_command, {
        label: 'Display SSH Info',
        isEnabled: () => true,
        execute: args => {
            (0,_funcs__WEBPACK_IMPORTED_MODULE_6__.checkSSH)();
        }
    });
    palette.addItem({ command: open_command, category: 'SSH' });
    console.log('JupyterLab user-workspace-management extension is activated!');
}
;
///////////////////////////////////////////////////////////////
//
// Display user info extension
//
///////////////////////////////////////////////////////////////
const extensionUser = {
    id: 'display_user_info',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette],
    activate: (app, palette) => {
        const open_command = 'sshinfo:user';
        app.commands.addCommand(open_command, {
            label: 'Display User Info',
            isEnabled: () => true,
            execute: args => {
                (0,_funcs__WEBPACK_IMPORTED_MODULE_6__.checkUserInfo)();
            }
        });
        palette.addItem({ command: open_command, category: 'User' });
        console.log('JupyterLab MAAP User Workspace Management extension is activated!');
    }
};
///////////////////////////////////////////////////////////////
//
// Presigned URL extension
//
///////////////////////////////////////////////////////////////
const extensionPreSigneds3Url = {
    id: 'share-s3-url',
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.IFileBrowserFactory, _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_3__.IStateDB],
    autoStart: true,
    activate: _funcs__WEBPACK_IMPORTED_MODULE_6__.activateGetPresignedUrl
};
///////////////////////////////////////////////////////////////
//
// Refresh token extension
//
// This plugin refreshes the users keycloak token on set time interval
// to extend the time a user can functionally use a workspace before
// having to manually refresh the page
//
///////////////////////////////////////////////////////////////
const extensionRefreshToken = {
    id: 'refresh_token',
    autoStart: true,
    requires: [],
    optional: [],
    activate: () => {
        // just called once at the beginning 
        setTimeout(() => (0,_getKeycloak__WEBPACK_IMPORTED_MODULE_7__.updateKeycloakToken)(300), 2000);
        // Refresh just under every 5 min, make token last for 5 min
        setInterval(() => (0,_getKeycloak__WEBPACK_IMPORTED_MODULE_7__.updateKeycloakToken)(300), 299000);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([extensionSsh, extensionUser, extensionPreSigneds3Url, extensionRefreshToken]);


/***/ }),

/***/ "./lib/request.js":
/*!************************!*\
  !*** ./lib/request.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DEFAULT_REQUEST_OPTIONS: () => (/* binding */ DEFAULT_REQUEST_OPTIONS),
/* harmony export */   request: () => (/* binding */ request)
/* harmony export */ });
const DEFAULT_REQUEST_OPTIONS = {
    ignoreCache: false,
    headers: {
        Accept: 'application/json, text/javascript, text/plain'
    },
    timeout: 5000,
};
function queryParams(params = {}) {
    return Object.keys(params)
        .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
        .join('&');
}
function withQuery(url, params = {}) {
    const queryString = queryParams(params);
    return queryString ? url + (url.indexOf('?') === -1 ? '?' : '&') + queryString : url;
}
function parseXHRResult(xhr) {
    return {
        ok: xhr.status >= 200 && xhr.status < 300,
        status: xhr.status,
        statusText: xhr.statusText,
        headers: xhr.getAllResponseHeaders(),
        data: xhr.responseText,
        json: () => JSON.parse(xhr.responseText),
        url: xhr.responseURL
    };
}
function errorResponse(xhr, message = null) {
    return {
        ok: false,
        status: xhr.status,
        statusText: xhr.statusText,
        headers: xhr.getAllResponseHeaders(),
        data: message || xhr.statusText,
        json: () => JSON.parse(message || xhr.statusText),
        url: xhr.responseURL
    };
}
function request(method, url, queryParams = {}, body = null, options = DEFAULT_REQUEST_OPTIONS) {
    const ignoreCache = options.ignoreCache || DEFAULT_REQUEST_OPTIONS.ignoreCache;
    const headers = options.headers || DEFAULT_REQUEST_OPTIONS.headers;
    const timeout = options.timeout || DEFAULT_REQUEST_OPTIONS.timeout;
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open(method, withQuery(url, queryParams));
        if (headers) {
            Object.keys(headers).forEach(key => xhr.setRequestHeader(key, headers[key]));
        }
        if (ignoreCache) {
            xhr.setRequestHeader('Cache-Control', 'no-cache');
        }
        xhr.timeout = timeout;
        xhr.onload = evt => {
            resolve(parseXHRResult(xhr));
        };
        xhr.onerror = evt => {
            resolve(errorResponse(xhr, 'Failed to make request.'));
        };
        xhr.ontimeout = evt => {
            resolve(errorResponse(xhr, 'Request took longer than expected.'));
        };
        if (method === 'post' && body) {
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify(body));
        }
        else {
            xhr.send();
        }
    });
}


/***/ }),

/***/ "./lib/selector.js":
/*!*************************!*\
  !*** ./lib/selector.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DropdownSelector: () => (/* binding */ DropdownSelector)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _funcs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./funcs */ "./lib/funcs.js");



class DropdownSelector extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    defaultOption;
    state;
    path;
    _dropdown;
    selected;
    constructor(options, defaultOption, state, path) {
        super();
        this.defaultOption = defaultOption;
        this.state = state;
        this.path = path;
        this._dropdown = document.createElement("SELECT");
        if (!defaultOption) {
            this.defaultOption = '';
        }
        let opt;
        for (let option of options) {
            opt = document.createElement("option");
            if (this.defaultOption === option) {
                opt.setAttribute("selected", "selected");
            }
            opt.setAttribute("id", option);
            opt.setAttribute("label", option);
            opt.appendChild(document.createTextNode(option));
            this._dropdown.appendChild(opt);
        }
        this.node.appendChild(this._dropdown);
    }
    getValue() {
        this.selected = this._dropdown.value;
        let ind = this.selected.indexOf('(');
        if (ind > -1) {
            this.selected = this.selected.substr(0, ind).trim();
        }
        // guarantee default value
        if (this.selected == null || this.selected == '') {
            this.selected = this.defaultOption;
            console.log('no option selected, using ' + this.defaultOption);
        }
        console.log(this.selected);
        // send request to get url
        (0,_funcs__WEBPACK_IMPORTED_MODULE_2__.getPresignedUrl)(this.state, this.path, this.selected).then((url) => {
            let display = url;
            let validUrl = false;
            if (url.substring(0, 5) == 'https') {
                validUrl = true;
                display = 'Link will expire in ' + this._dropdown.value + '<br>';
                display = display + '<a href=' + url + ' target="_blank" style="border-bottom: 1px solid #0000ff; color: #0000ff;">' + url + '</a>';
            }
            else {
                display = url;
            }
            let body = document.createElement('div');
            body.style.display = 'flex';
            body.style.flexDirection = 'column';
            let textarea = document.createElement("div");
            textarea.id = 'result-text';
            textarea.style.display = 'flex';
            textarea.style.flexDirection = 'column';
            textarea.innerHTML = "<pre>" + display + "</pre>";
            body.appendChild(textarea);
            // Copy URL to clipboard button if url created
            if (validUrl) {
                let copyBtn = document.createElement('button');
                copyBtn.id = 's3-link-copy-button';
                copyBtn.className = 'jupyter-button';
                copyBtn.innerHTML = 'Copy Link';
                copyBtn.style.width = "200px";
                copyBtn.addEventListener('click', function () {
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Clipboard.copyToSystem(url);
                }, false);
                body.appendChild(copyBtn);
            }
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: 'Presigned Url',
                body: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget({ node: body }),
                focusNodeSelector: 'input',
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'Ok' })]
            });
        });
    }
}


/***/ }),

/***/ "./lib/widgets.js":
/*!************************!*\
  !*** ./lib/widgets.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   InjectSSH: () => (/* binding */ InjectSSH),
/* harmony export */   SshWidget: () => (/* binding */ SshWidget),
/* harmony export */   UserInfoWidget: () => (/* binding */ UserInfoWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _request__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./request */ "./lib/request.js");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _getKeycloak__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./getKeycloak */ "./lib/getKeycloak.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);





class SshWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor() {
        let body = document.createElement('div');
        body.style.display = 'flex';
        body.style.flexDirection = 'column';
        (0,_request__WEBPACK_IMPORTED_MODULE_3__.request)('get', _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getBaseUrl() + "jupyter-server-extension/uwm/getSSHInfo").then((res) => {
            if (res.ok) {
                let json_results = res.json();
                let ip = json_results['ip'];
                let port = json_results['port'];
                let message = "ssh root@" + ip + " -p " + port;
                // let message = "ssh -i <path_to_your_key> root@" + ip + " -p " + port;
                let contents = document.createTextNode(message);
                body.appendChild(contents);
            }
        });
        super({ node: body });
    }
}
class UserInfoWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(username, email, org) {
        let body = document.createElement('div');
        body.style.display = 'flex';
        body.style.flexDirection = 'column';
        let user_node = document.createTextNode('Username: ' + username);
        body.appendChild(user_node);
        body.appendChild(document.createElement('br'));
        let email_node = document.createTextNode('Email: ' + email);
        body.appendChild(email_node);
        body.appendChild(document.createElement('br'));
        let org_node = document.createTextNode('Organization: ' + org);
        body.appendChild(org_node);
        super({ node: body });
    }
}
class InjectSSH {
    constructor() {
        (0,_getKeycloak__WEBPACK_IMPORTED_MODULE_4__.getUserInfo)(function (profile) {
            var getUrl = new URL(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getBaseUrl() + 'jupyter-server-extension/uwm/getAccountInfo');
            getUrl.searchParams.append("proxyGrantingTicket", profile['proxyGrantingTicket']);
            var xhr = new XMLHttpRequest();
            xhr.onload = function () {
                if (xhr.status == 200) {
                    let key = '';
                    try {
                        let response = JSON.parse(xhr.response);
                        key = response["profile"]["public_ssh_key"];
                    }
                    catch (error) {
                        console.log("Bad response from jupyter-server-extension/uwm/getAccountInfo");
                    }
                    if (key == undefined || profile == undefined || profile['proxyGrantingTicket'] == undefined) {
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Notification.warning("User's SSH Key undefined. SSH service unavailable.");
                    }
                    else {
                        let getUrlInjectPublicKey = new URL(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getBaseUrl() + "jupyter-server-extension/uwm/injectPublicKey");
                        getUrlInjectPublicKey.searchParams.append("key", key);
                        let xhrInjectPublicKey = new XMLHttpRequest();
                        xhrInjectPublicKey.onload = function () {
                            console.log("Checked for/injected user's public key");
                        };
                        xhrInjectPublicKey.open("GET", getUrlInjectPublicKey.href, true);
                        xhrInjectPublicKey.send(null);
                    }
                    if (profile != undefined) {
                        let getUrlInjectPGT = new URL(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getBaseUrl() + "jupyter-server-extension/uwm/injectPGT");
                        getUrlInjectPGT.searchParams.append("proxyGrantingTicket", profile['proxyGrantingTicket']);
                        let xhrInjectPGT = new XMLHttpRequest();
                        xhrInjectPGT.onload = function () {
                            console.log("Checked for/injected user's PGT");
                        };
                        xhrInjectPGT.open("GET", getUrlInjectPGT.href, true);
                        xhrInjectPGT.send(null);
                    }
                    else {
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Notification.warning("Profile not defined so PGT token not set. Some services may be unavailable.");
                    }
                }
                else {
                    console.log("Error making call to account profile. Status is " + xhr.status + ". Was your MAAP PGT token properly set?");
                }
            };
            xhr.onerror = function () {
                console.log("Error making call to account profile. Status is " + xhr.status + ". Was your MAAP PGT token properly set?");
            };
            xhr.open("GET", getUrl.href, true);
            xhr.send(null);
        });
    }
}


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./style/index.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.79a760ba4b3703b8e5b4.js.map