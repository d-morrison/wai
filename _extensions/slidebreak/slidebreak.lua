function slidebreak()
  local format = quarto.doc.is_format

  if format("revealjs") or format("pptx") or format("powerpoint") then
    return pandoc.HorizontalRule()
  end

  return pandoc.Null()
end

return {
  ["slidebreak"] = slidebreak
}
