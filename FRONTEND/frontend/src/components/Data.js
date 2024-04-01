import React, { useState, useEffect, useRef } from "react";

const API = process.env.REACT_APP_API;

export const Data = () => {
    const [YearStart, setYearStart] = useState("");
    const [YearEnd, setYearEnd] = useState("");
    const [LocationDesc, setLocationDesc] = useState("");
    const [Topic, setTopic] = useState("");

    const [editing, setEditing] = useState(false);
    const [id, setId] = useState("");

    const nameInput = useRef(null);

    let [data2, setData2] = useState([]);

    const cityMappings = {
        "quito": "uio",
        "new york": "ny",
        // Agrega más mapeos según sea necesario
    };

    // Obtener el valor mapeado correspondiente o utilizar el valor original si no hay mapeo definido
    const mappedLocation = cityMappings[LocationDesc.toLowerCase()] || LocationDesc;



    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!editing) {
            const res = await fetch(`${API}/api/data`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    YearStart,
                    YearEnd,
                    LocationDesc,
                    Topic,


                }),

            });
            await res.json();
            window.location.reload();


        } else {
            const res = await fetch(`${API}/api/data/${id.$oid}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    YearStart,
                    YearEnd,
                    LocationDesc,
                    Topic,
                }),
            });
            const data = await res.json();
            console.log(data);
            setEditing(false);
            setId("");

        }


        setYearStart("");
        setYearEnd("");
        setLocationDesc("");
        setTopic("");
        nameInput.current.focus();
        window.location.reload();
    };

    const getData2 = async () => {
        const res = await fetch(`${API}/api/data`);
        const data = await res.json();
        setData2(data);
    };

    const deleteDat = async (id) => {
        const userResponse = window.confirm("Are you sure you want to delete it?");
        if (userResponse) {
            console.log(id.$oid);
            const res = await fetch(`${API}/api/data/${id.$oid}`, {
                method: "DELETE",
            });
            const data = await res.json();
            console.log(data);
            await getData2();
        }
    };

    const editDat = async (id) => {
        const res = await fetch(`${API}/api/data/${id.$oid}`);
        const data = await res.json();

        setEditing(true);
        setId(id);

        // Reset
        setYearStart(data.YearStart);
        setYearEnd(data.YearEnd);
        setLocationDesc(data.LocationDesc);
        setTopic(data.Topic);
        nameInput.current.focus();


    };

    const styles = {
        body: {
            margin: 0,
            padding: 0,
            background: "url('https://cdn.pixabay.com/photo/2015/02/25/09/12/brook-648512_1280.jpg') no-repeat center center fixed",
            backgroundSize: "cover",
            fontFamily: "Arial, sans-serif",
            color: "#fff",
        }
    };

    useEffect(() => {
        getData2();
    }, []);

    return (
        <div className="row">
            <div className="col-md-4">
                <form onSubmit={handleSubmit} className="card card-body">
                    <div className="form-group">
                        <input
                            type="number"
                            onChange={(e) => setYearStart(e.target.value)}
                            value={YearStart}
                            className="form-control"
                            placeholder="YearStart"
                            ref={nameInput}
                            autoFocus
                        />
                    </div>
                    <div className="form-group">
                        <input
                            type="number"
                            onChange={(e) => setYearEnd(e.target.value)}
                            value={YearEnd}
                            className="form-control"
                            placeholder="YearEnd"
                        />
                    </div>
                    <div className="form-group">
                        <input
                            type="text"
                            onChange={(e) => setLocationDesc(e.target.value)}
                            value={LocationDesc}
                            className="form-control"
                            placeholder="Location"
                        />
                    </div>
                    <div className="form-group">
                        <input
                            type="text"
                            onChange={(e) => setTopic(e.target.value)}
                            value={Topic}
                            className="form-control"
                            placeholder="Topic"
                        />
                    </div>
                    <button className="btn btn-primary btn-block">
                        {editing ? "Update" : "Create"}
                    </button>
                </form>
            </div>
            <div className="col-md-6">
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>YearStart</th>
                            <th>YearEnd</th>
                            <th>Location</th>
                            <th>Topic</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data2.map((dat) => (
                            <tr key={dat._id}>
                                <td>{dat.YearStart}</td>
                                <td>{dat.YearEnd}</td>
                                <td>{dat.LocationDesc}</td>
                                <td>{dat.Topic}</td>
                                <td>
                                    <button
                                        className="btn btn-secondary btn-sm btn-block"
                                        onClick={(e) => editDat(dat._id)}
                                    >
                                        Edit
                                    </button>
                                    <button
                                        className="btn btn-danger btn-sm btn-block"
                                        onClick={(e) => deleteDat(dat._id)}
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};