import Vue from 'vue'

export function showToast(msg, type, duration) {

  var dur
  if (!duration === undefined) {
    dur = duration
  } else {
    if (type === "error" || type === "info") {
      dur = 3000
    } else {
      dur = 2000
    }
  }
  

  Vue.toasted.show(msg, {
    action: [
      {
        text: "Ok",
        onClick: (e, toastObject) => {
          toastObject.goAway(0);
        },
      },
    ],
    position: "top-center",
    type: type,
    duration: dur,
    theme: "bubble",
    keepOnHover: true,
    className: "toast",
    containerClass: "toast",
  });
}