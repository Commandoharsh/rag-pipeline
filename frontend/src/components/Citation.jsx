function Citation({ citation }) {

    return (
        <div className="citation">

            <strong>
                {citation.source}
            </strong>

            <span>
                Page {citation.page}
            </span>

            <small>
                {citation.chunk_id}
            </small>

        </div>
    );
}

export default Citation;