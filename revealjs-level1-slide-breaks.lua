function Pandoc(doc)
  if not string.match(FORMAT, "revealjs") then
    return doc
  end

  local updated_blocks = {}

  for i, block in ipairs(doc.blocks) do
    table.insert(updated_blocks, block)

    if block.t == "Header" and block.level <= 2 then
      local next_block = doc.blocks[i + 1]

      if next_block and next_block.t ~= "HorizontalRule" then
        table.insert(updated_blocks, pandoc.HorizontalRule())
      end
    end
  end

  return pandoc.Pandoc(updated_blocks, doc.meta)
end
