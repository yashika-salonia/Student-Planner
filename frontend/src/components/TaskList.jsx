import React, { useState, useEffect } from "react";
import { taskAPI } from "../services/api";

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({ title: "", description: "" });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    const response = await taskAPI.getAll();
    setTasks(response.data);
  };

  const createTask = async () => {
    await taskAPI.create({ ...newTask, status: "pending" });
    setNewTask({ title: "", description: "" });
    fetchTasks();
  };

  const updateStatus = async (id, status) => {
    await taskAPI.update(id, { status });
    fetchTasks();
  };

  const deleteTask = async (id) => {
    await taskAPI.delete(id);
    fetchTasks();
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-6">Tasks</h2>

      {/* Create Form */}
      <div className="mb-6 p-4 bg-gray-50 rounded">
        <input
          type="text"
          placeholder="Task title"
          value={newTask.title}
          onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
          className="w-full p-2 border rounded mb-2"
        />
        <textarea
          placeholder="Description"
          value={newTask.description}
          onChange={(e) =>
            setNewTask({ ...newTask, description: e.target.value })
          }
          className="w-full p-2 border rounded mb-2"
        />
        <button
          onClick={createTask}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Add Task
        </button>
      </div>

      {/* Task List */}
      <div className="space-y-4">
        {tasks.map((task) => (
          <div
            key={task.id}
            className="p-4 border rounded hover:shadow-md transition"
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h3 className="font-semibold text-lg">{task.title}</h3>
                <p className="text-gray-600">{task.description}</p>
                <span
                  className={`inline-block mt-2 px-3 py-1 rounded text-sm ${
                    task.status === "completed"
                      ? "bg-green-100 text-green-800"
                      : "bg-yellow-100 text-yellow-800"
                  }`}
                >
                  {task.status}
                </span>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() =>
                    updateStatus(
                      task.id,
                      task.status === "pending" ? "completed" : "pending",
                    )
                  }
                  className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300"
                >
                  Toggle
                </button>
                <button
                  onClick={() => deleteTask(task.id)}
                  className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TaskList;
