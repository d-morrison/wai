local theorem_div_classes = {
  "thm",
  "theorem",
  "lem",
  "lemma",
  "cor",
  "corollary",
  "prp",
  "proposition",
  "cnj",
  "conjecture",
  "def",
  "definition",
  "exm",
  "example",
  "exr",
  "exercise",
  "proof",
  "remark",
  "solution"
}

local function class_is_theorem_like(class)
  for _, theorem_class in ipairs(theorem_div_classes) do
    if class == theorem_class then
      return true
    end
  end

  return false
end

local function is_theorem_div(div)
  for _, class in ipairs(div.classes) do
    if class_is_theorem_like(class) then
      return true
    end
  end

  return false
end

local function has_class(div, class_name)
  for _, class in ipairs(div.classes) do
    if class == class_name then
      return true
    end
  end

  return false
end

local function read_anchor_script()
  local filter_dir = pandoc.path.directory(PANDOC_SCRIPT_FILE)
  local script_path = pandoc.path.join({ filter_dir, "div-anchors.js" })
  local script_file = io.open(script_path, "r")

  if not script_file then
    return nil
  end

  local script = script_file:read("*a")
  script_file:close()
  return script
end

function Div(div)
  if not quarto.doc.is_format("html") or quarto.doc.is_format("revealjs") then
    return nil
  end

  if div.identifier == "" or not is_theorem_div(div) then
    return nil
  end

  if not has_class(div, "anchored") then
    div.classes:insert("anchored")
  end

  if not div.attributes["data-anchor-id"] then
    div.attributes["data-anchor-id"] = div.identifier
  end

  return div
end

function Pandoc(doc)
  if not quarto.doc.is_format("html") or quarto.doc.is_format("revealjs") then
    return doc
  end

  local anchor_script = read_anchor_script()
  if not anchor_script or anchor_script == "" then
    return doc
  end

  doc.blocks:insert(pandoc.RawBlock("html", anchor_script))
  return doc
end
