function getEventSrc(e) {
  // get a reference to the IE/windows event object
  if (!e) {
    e = window.event;
  }

  if (e.target) {
    // DOM-compliant name of event source property
    return e.target;
  } else if (e.srcElement) {
    // IE/windows name of event source property
    return e.srcElement;
  } else {
    return null;
  }
}

// New in firefox 1.5
window.onpageshow = initXForms;
window.onload = initXForms;

function initXForms() {
	var form = document.forms[1];
	if (form) {
  	for (var i=0; i < form.elements.length; i++) {
  		if (form.elements[i].disabled == true) {
  		    if (form.elements[i].oldvalue) {
  		        form.elements[i].value = form.elements[i].oldvalue;
  		    }
  		    form.elements[i].disabled = false;
  		}
  	}
  }
}
//
// Process the XForm submission
//
function submitForm(form, modelid, submissionid) {
    var usedElements = [];
    var imElements = [];
    var saction = '__submission_action+'+modelid+'+'+submissionid
    var smethod = '__submission_method+'+modelid+'+'+submissionid
    var starget = '__submission_target+'+modelid+'+'+submissionid
    // This is basically a hack, because, for some reason, early mozilla
    // versions seem to supress the value of the submitted button when
    // the onclick event is raised
   form.__submit__.value = modelid+'+'+submissionid
   for (var i=0; i < form.elements.length; i++) {
        if (form.elements[i].name == saction) {
            form.action = form.elements[i].value;
        }
        else if (form.elements[i].name == smethod) {
            if (form.elements[i].value == 'form-data-post') {
                form.method = 'POST';
                form.enctype = 'multipart/form-data';
                // IE, for some reason, handles this differently
                form.encoding = 'multipart/form-data';
            }
            else if (form.elements[i].value == 'urlencoded-post') {
                form.method = 'POST';
                form.enctype = 'application/x-www-form-urlencoded';
                // IE, for some reason, handles this differently
                form.encoding = 'application/x-www-form-urlencoded';
            }
            else {
                form.method = 'GET';
            }
        }
        else if (form.elements[i].name == starget) {
            form.target = form.elements[i].value;
        }
		
         // Set up the real form elements for submission, and delete
         // the placeholders
         currElement = form.elements[i];
         try {
             var eparts = currElement.name.split('+')
             if (eparts[0] == modelid) {
                 currElement.name = eparts[1];
                 usedElements.push(currElement.name);
             };
             if (eparts[0] == '__instance' && eparts[1] == modelid) {
                 imElements.push(currElement);
             };
             // we don't want this node to appear in the submission
             if (currElement.name != eparts[1] && currElement.name.indexOf('__submit') != 0) {
                 currElement.disabled = true;
             }
         }
         catch (e) {}
    }

    // figure out which elements we've used, and which are supposed
    // to be 'automatically' submitted as hidden elements
    var uLen = usedElements.length;
    var imLen = imElements.length;
    for (var i=0; i < imLen; i++) {
        var imElement = imElements[i];
        var imParts = imElement.name.split('+');
        var used = false;
        for (var j=0; j < uLen; j++) {
            if (usedElements[j] == imParts[2]) {
                used = true;
                break;
            }
        }
        if (used == false) {
            imElement.name = imParts[2];
            imElement.disabled = false;
        }
    }
	
    form.submit();

    return true;
};

function submitButtonHandler(submitter) {
    var sparts = submitter.name.split('+');
    var sname = sparts[0];
    var modelid = sparts[1];
    var submissionid = sparts[2];
	
	submitter.oldvalue = submitter.value;
	submitter.value = 'Processing - Please Wait ...'
	submitter.disabled = true;
	
    return submitForm(submitter.form, modelid, submissionid);
}

function keypressEventHandler(form, event) {
    target = getEventSrc(event);
    var sparts = target.name.split('+');
    var modelid = sparts[0];
    var submissionid = '';
    
    if (event.keyCode == 13) {
    	// don't submit on textareas, very bad!
        if (event.target.type == 'textarea') {
        	return true;
        }
        submissionid = getSubmissionId(modelid, form);
        submitForm(form, modelid, submissionid);
        return false;
    }
    return true;
}

//------------------------------------------------------------------------------
// getSubmissionId - gets the submission id of a form.
//------------------------------------------------------------------------------
function getSubmissionId (modelid, form) {
    for (var i=0; i < form.elements.length; i++) {
        var eparts = form.elements[i].name.split('+');
        if (eparts[0] == '__submission_action' && eparts[1] == modelid) {
            return (eparts[2]);
        }
    }

    // Submission ID not found.
    return ('');
}

//------------------------------------------------------------------------------
// ToggleNavigationVisibility - toggles the visibility of a single object in the
// site navigation.
//------------------------------------------------------------------------------
function ToggleNavigationVisibility (modelid, id, submissionid) {
    // Check the corresponding checkbox.
    var checkboxid = modelid + '-' + id;
    var checkbox = document.getElementById(checkboxid);
    checkbox.checked = true;

    // Get the form containing this element.
    var parent = checkbox;
    while (parent == parent.parentNode) {
        if (parent.tagName == 'FORM') break;
    }
    if (!parent) {
        return (false);
    }
    else {
        var form = parent;
    }

    // Submit the form.
    submitForm(form, modelid, submissionid);
    return (false);
}

//------------------------------------------------------------------------------
// SubmitParentForm - submits the form containing this element.
//------------------------------------------------------------------------------
function SubmitParentForm (el, modelid, submissionid) {

    // Get the form containing this element.
    var parent = el;
    while (parent == parent.parentNode) {
        if (parent.tagName == 'FORM') break;
    }
    if (!parent) {
        return (false);
    }
    else {
        var form = parent;
    }

    // Submit the form.
    submitForm(form, modelid, submissionid);
    return (false);
}
