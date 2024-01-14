import React from "react";

export function MediaInput({accept, onChange, multiple, id, text, directory}) {
    return (
        <div>
            <input
                type="file"
                accept={accept + '/*'}
                onChange={onChange}
                hidden
                multiple={multiple}
                id={id}
                {...(directory ? {webkitdirectory: ""} : {})}

            />
            <label htmlFor={id} className="upload-button">{text}</label>
        </div>
    )
}