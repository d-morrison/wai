local function in_html_output()
  if quarto and quarto.doc and quarto.doc.is_format then
    return quarto.doc.is_format("html") or quarto.doc.is_format("revealjs")
  end

  return false
end

local function anchor_script()
  return [[
<script>
const defaultAnchorIconFallback = "#";

function getDefaultAnchorTemplate() {
  const defaultAnchor = document.querySelector("a.anchorjs-link[data-anchorjs-icon]");
  if (!defaultAnchor) {
    return null;
  }

  return {
    icon: defaultAnchor.getAttribute("data-anchorjs-icon"),
    style: defaultAnchor.getAttribute("style")
  };
}

function alignEquationAnchorWithDefault(anchor, template) {
  if (!anchor) {
    return;
  }

  anchor.classList.remove("external");

  if (template && template.icon) {
    anchor.setAttribute("data-anchorjs-icon", template.icon);
    anchor.textContent = "";
  } else if (!anchor.textContent) {
    anchor.textContent = defaultAnchorIconFallback;
  }

  if (template && template.style) {
    anchor.setAttribute("style", template.style);
  } else {
    anchor.removeAttribute("style");
  }
}

function alignEquationAnchorsWithDefault() {
  const template = getDefaultAnchorTemplate();
  document.querySelectorAll("a.equation-anchor").forEach(function (anchor) {
    alignEquationAnchorWithDefault(anchor, template);
  });
}

document.addEventListener("DOMContentLoaded", function () {
  const equations = document.querySelectorAll("span[id^='eq-']");
  equations.forEach(function (equation) {
    if (equation.querySelector(".equation-anchor")) {
      return;
    }

    if (!equation.querySelector(".math.display")) {
      return;
    }

    const id = equation.getAttribute("id");
    if (!id) {
      return;
    }

    equation.classList.add("equation-anchor-target");

    const anchor = document.createElement("a");
    anchor.className = "equation-anchor anchorjs-link";
    anchor.href = "#" + id;
    anchor.setAttribute("aria-label", "Permalink to this equation");
    equation.appendChild(anchor);
  });

  alignEquationAnchorsWithDefault();
});

window.addEventListener("load", alignEquationAnchorsWithDefault);
</script>
]]
end

function Pandoc(doc)
  if not in_html_output() then
    return nil
  end

  table.insert(doc.blocks, pandoc.RawBlock("html", anchor_script()))
  return doc
end
