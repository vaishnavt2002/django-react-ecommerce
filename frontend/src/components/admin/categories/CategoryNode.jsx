import CategoryTree from "./CategoryTree";
import { useState } from "react";

export default function CategoryNode({
    node,
    level,
    onAdd,
    onEdit,
    onDeactivate,
}) {
    const [expanded, setExpanded] = useState(true);

    return (
        <div>
            <div
                className="flex items-center justify-between py-2 hover:bg-gray-50 rounded-md px-2"
                style={{ paddingLeft: `${level * 20}px` }}
            >
                <div className="flex items-center gap-2">
                    {node.children?.length > 0 && (
                        <button
                            onClick={() => setExpanded(!expanded)}
                            className="text-gray-500 text-xs"
                        >
                            {expanded ? "▼" : "▶"}
                        </button>
                    )}

                    <span
                        className={`${node.is_active ? "" : "text-gray-400 line-through"
                            }`}
                    >
                        {node.name}
                    </span>
                </div>

                <div className="flex gap-4 text-sm">
                    <button
                        onClick={() => onAdd(node)}
                        className="text-green-600 hover:underline"
                    >
                        Add
                    </button>

                    <button
                        onClick={() => onEdit(node)}
                        className="text-blue-600 hover:underline"
                    >
                        Edit
                    </button>

                    {node.is_active && (
                        <button
                            onClick={() => onDeactivate(node.id)}
                            className="text-red-600 hover:underline"
                        >
                            Deactivate
                        </button>
                    )}
                </div>
            </div>

            {expanded && node.children?.length > 0 && (
                <CategoryTree
                    nodes={node.children}
                    level={level + 1}
                    onAdd={onAdd}
                    onEdit={onEdit}
                    onDeactivate={onDeactivate}
                />
            )}
        </div>
    );
}