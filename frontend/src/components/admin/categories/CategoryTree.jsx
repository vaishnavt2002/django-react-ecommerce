import CategoryNode from "./CategoryNode";

export default function CategoryTree({
    nodes = [],
    level = 0,
    onAdd,
    onEdit,
    onDeactivate,
}) {
    if (!Array.isArray(nodes)) return null;

    return (
        <>
            {nodes.map((node) => (
                <CategoryNode
                    key={node.id}
                    node={node}
                    level={level}
                    onAdd={onAdd}
                    onEdit={onEdit}
                    onDeactivate={onDeactivate}
                />
            ))}
        </>
    );
}