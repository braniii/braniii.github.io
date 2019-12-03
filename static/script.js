const switchColor = () => {
  const html = document.getElementsByTagName("html")[0];
  const colorSwitcher = document.getElementById("color-switcher");
  if (html.classList.contains("dark")) {
    html.classList.remove("dark");
    colorSwitcher.innerHTML = "dark mode";
    window.localStorage.setItem("color", "light");
  } else {
    html.classList.add("dark");
    colorSwitcher.innerHTML = "light mode";
    window.localStorage.setItem("color", "dark");
  }
};

const restoreColor = () => {
  const color = window.localStorage.getItem("color");
  if (color == "dark") {
    const html = document.getElementsByTagName("html")[0];
    html.classList.add("dark");

    window.onload = () => {
      const colorSwitcher = document.getElementById("color-switcher");
      colorSwitcher.innerHTML = "light mode";
    };
  }
};
