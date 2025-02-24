import asyncio
import json

import uvicorn
from fastapi import FastAPI, APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


def get_last_n_queued_requests(redis_client, limit: int = 100):
    """
    Fetch the `limit` most recently queued requests (tasks) in descending order.
    """
    if limit < 1:
        limit = 1
    if limit > 100:
        limit = 100

    # Grab up to `limit` task IDs by descending score (newest first).
    task_ids = redis_client.zrevrange("queued_requests", 0, limit - 1)

    queued_tasks = []
    for tid in task_ids:
        # Load the full task details from "task:{task_id}"
        task_json = redis_client.get(f"task:{tid}")
        if task_json:
            try:
                task_data = json.loads(task_json)
                queued_tasks.append(task_data)
            except json.JSONDecodeError:
                continue

    return queued_tasks


class Analytics:
    """
    A small FastAPI-based API for ModelQ-like data, encapsulated in a class.
    """

    def __init__(self, redis_client, host="127.0.0.1", port=5566):
        """
        :param redis_client: an existing Redis instance
        """
        self.redis = redis_client
        self.host = host
        self.port = port

        # Create the FastAPI app
        self.app = FastAPI(title="ModelQ Dashboard")

        # Create a router to group our /api endpoints
        api_router = APIRouter()

        @api_router.get("/")
        def root():
            return {"message": "Welcome to the ModelQ Analytics API!"}

        @api_router.get("/task/{task_id}")
        def get_task_by_id(task_id: str):
            task_key = f"task:{task_id}"
            data = self.redis.get(task_key)
            if not data:
                raise HTTPException(status_code=404, detail="Task not found")
            task_data = json.loads(data)
            return task_data

        @api_router.get("/queue_stats")
        def queue_stats():
            return self.get_queue_stats()

        @api_router.get("/workers")
        def worker_statuses():
            return self.get_workers()

        @api_router.get("/queued_requests")
        def queued_requests(limit: int = Query(100, ge=1, le=100)):
            return get_last_n_queued_requests(self.redis, limit=limit)

        # -------------------- NEW WEBSOCKET ROUTE --------------------
        @api_router.websocket("/ws/dashboard")
        async def websocket_dashboard(websocket: WebSocket):
            """
            A WebSocket endpoint that periodically sends updated dashboard data
            (queue stats, worker statuses, etc.) to the connected client.
            """
            await websocket.accept()
            try:
                while True:
                    # Collect the latest data and send as JSON
                    data = {
                        "stats": self.get_queue_stats(),
                        "workers": self.get_workers(),
                        # Optionally also send queued requests if desired:
                        # "tasks": get_last_n_queued_requests(self.redis, limit=10),
                    }
                    await websocket.send_json(data)
                    await asyncio.sleep(2)  # Broadcast update every 2 seconds
            except WebSocketDisconnect:
                print("WebSocket disconnected")

        # -------------------------------------------------------------

        # Include our router
        self.app.include_router(api_router, prefix="/api")

        @self.app.get("/", response_class=HTMLResponse)
        def dashboard():
            return HTMLResponse(self.render_dashboard())

    def get_queue_stats(self):
        """
        Helper method to return the queue stats as a dict.
        """
        queued_count = self.redis.scard("queued_tasks") or 0
        processing_count = self.redis.scard("processing_tasks") or 0
        ml_tasks_count = self.redis.llen("ml_tasks") or 0
        active_workers_count = len(self.redis.hkeys("servers"))

        return {
            "queued_count": queued_count,
            "processing_count": processing_count,
            "ml_tasks_count": ml_tasks_count,
            "active_workers_count": active_workers_count,
        }

    def get_workers(self):
        """
        Helper method that returns the workers data as a dict
        (similar to /api/workers endpoint).
        """
        workers_data = {}
        server_keys = self.redis.hkeys("servers")
        for server_id in server_keys:
            val = self.redis.hget("servers", server_id)
            if val:
                workers_data[server_id] = json.loads(val)
        return workers_data

    def render_dashboard(self):
        """
        Returns the entire HTML for the ModelQ Dashboard, including:
        - Worker Status tab
        - Requests tab
        - WebSocket-based updates for real-time data
        - A modal for displaying task details (with "X" close and "Copy JSON" button)
        """
        return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>ModelQ Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="bg-gray-50 text-gray-800">
  <div class="container mx-auto py-6">
    <!-- Header and Search -->
    <header class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold">ModelQ Dashboard</h1>
      <div class="flex">
        <input
          type="text" 
          id="task_id" 
          placeholder="Search Task ID"
          class="border border-gray-300 rounded-l-md px-4 py-2 text-sm 
                 focus:outline-none focus:ring-2 focus:ring-gray-200"
        />
        <button
          onclick="getTask()"
          class="bg-black text-white rounded-r-md px-6 py-2 text-sm 
                 hover:bg-gray-900 transition-colors duration-200"
        >
          Search
        </button>
      </div>
    </header>

    <!-- Stats Section -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <!-- Card: Requests in Queue -->
      <div class="bg-white rounded-xl shadow-sm hover:shadow-xl transition-all duration-200 p-6">
        <div class="flex items-center justify-between">
          <div class="space-y-2">
            <h2 class="text-sm font-medium text-gray-500">
              Requests in Queue
            </h2>
            <p id="ml_tasks_count" class="text-3xl font-bold tracking-tight text-gray-900">
              0
            </p>
          </div>
          <div class="rounded-full bg-blue-50 p-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-500" fill="none" 
                 viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M20 13V6a2 2 0 00-2-2H6a2 2 0
                       00-2 2v7m16 0v5a2 2 0
                       01-2 2H6a2 2 0
                       01-2-2v-5m16 0h-2.586
                       a1 1 0
                       00-.707.293l-2.414 2.414a1 1 0
                       01-.707.293
                       h-3.172a1 1 0
                       01-.707-.293l-2.414-2.414
                       A1 1 0
                       006.586 13H4" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Card: Requests Processed -->
      <div class="bg-white rounded-xl shadow-sm hover:shadow-xl transition-all duration-200 p-6">
        <div class="flex items-center justify-between">
          <div class="space-y-2">
            <h2 class="text-sm font-medium text-gray-500">
              Requests Processed
            </h2>
            <p id="processing_count" class="text-3xl font-bold tracking-tight text-gray-900">
              0
            </p>
          </div>
          <div class="rounded-full bg-green-50 p-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-500" fill="none"
                 viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0
                       11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Card: Active Workers -->
      <div class="bg-white rounded-xl shadow-sm hover:shadow-xl transition-all duration-200 p-6">
        <div class="flex items-center justify-between">
          <div class="space-y-2">
            <h2 class="text-sm font-medium text-gray-500">
              Active Workers
            </h2>
            <p id="active_workers" class="text-3xl font-bold tracking-tight text-gray-900">
              0
            </p>
          </div>
          <div class="rounded-full bg-purple-50 p-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-purple-500" fill="none" 
                 viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0
                       002-2V5a2 2 0 
                       00-2-2H5a2 2 0 
                       00-2 2v10
                       a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabs for Worker Status / Requests -->
    <div class="flex space-x-4 mb-4 border-b border-gray-300">
      <button id="tab-workers" 
              class="py-2 px-4 border-b-2 border-black text-black focus:outline-none"
              onclick="switchTab('workers')">
        Worker Status
      </button>
      <button id="tab-requests" 
              class="py-2 px-4 border-b-2 border-transparent text-gray-500 hover:text-black focus:outline-none"
              onclick="switchTab('requests')">
        Requests
      </button>
    </div>

    <!-- Workers Section (Tab Content) -->
    <section id="workers_section">
      <h2 class="text-2xl font-semibold mb-4">Worker Status</h2>
      <table class="min-w-full bg-white shadow rounded-lg">
        <thead>
          <tr>
            <th class="py-2 px-4 text-left text-sm font-medium text-gray-500 border-b">#</th>
            <th class="py-2 px-4 text-left text-sm font-medium text-gray-500 border-b">Worker ID</th>
            <th class="py-2 px-4 text-left text-sm font-medium text-gray-500 border-b">Status</th>
            <th class="py-2 px-4 text-left text-sm font-medium text-gray-500 border-b">Last Active</th>
          </tr>
        </thead>
        <tbody id="workers_table">
          <!-- Worker Rows Dynamically Inserted Here -->
        </tbody>
      </table>
    </section>

    <!-- Requests Section (Tab Content; hidden by default) -->
    <section id="requests_section" class="hidden">
      <h2 class="text-2xl font-semibold mb-4">Last 100 Requests</h2>

      <!-- Dropdown to select how many results to show -->
      <div class="flex items-center mb-4">
        <label for="request_limit" class="mr-2 text-sm">Show:</label>
        <select id="request_limit" class="border border-gray-300 rounded px-2 py-1 text-sm"
                onchange="getQueuedRequests()">
          <option value="10">10</option>
          <option value="50">50</option>
          <option value="100" selected>100</option>
        </select>
        <span class="ml-1 text-sm">requests</span>
      </div>

      <table class="min-w-full bg-white shadow rounded-lg">
        <thead>
          <tr>
            <th class="py-2 px-4 text-left text-sm font-medium text-gray-500 border-b">#</th>
            <th class="py-2 px-4 text-left text-sm font-medium text-gray-500 border-b">Request ID</th>
            <th class="py-2 px-4 text-left text-sm font-medium text-gray-500 border-b">Status</th>
            <th class="py-2 px-4 text-left text-sm font-medium text-gray-500 border-b">Queued Time</th>
          </tr>
        </thead>
        <tbody id="requests_table">
          <!-- Requests Rows Dynamically Inserted Here -->
        </tbody>
      </table>
    </section>
  </div>

  <!-- Modal (Task Details) -->
  <div id="taskModal" 
       class="fixed inset-0 bg-black bg-opacity-50 hidden 
              flex items-center justify-center z-50 p-4">
    <div class="bg-white w-full max-w-3xl rounded shadow-lg relative p-6 
                flex flex-col">

      <!-- Header with Close & Copy JSON -->
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Task Details</h2>
        <div class="space-x-2">
          <!-- Copy JSON button -->
          <button class="bg-blue-500 hover:bg-blue-600 text-white 
                         px-3 py-1 rounded text-sm"
                  onclick="copyTaskJson()">
            Copy JSON
          </button>
          <!-- Close Button -->
          <button class="text-gray-500 hover:text-gray-700 text-xl" 
                  onclick="hideTaskModal()">
            &times;  <!-- '×' symbol -->
          </button>
        </div>
      </div>

      <!-- Body: code block with JSON data 
           Use max-h to limit the size, allow scrolling -->
      <div class="bg-gray-100 rounded p-3 overflow-auto max-h-[80vh]">
        <pre class="text-sm leading-snug">
<code id="taskJson" class="whitespace-pre-wrap"></code>
        </pre>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer class="text-center text-gray-500 mt-8">
    &copy; 2025 ModelQ Analytics. All rights reserved.
  </footer>

  <script>
    let dashboardSocket = null;

    // On page load, initialize WebSocket and set default tab
    window.onload = () => {
      initDashboardWebSocket();
      // Default to Worker tab (or Requests tab, if you prefer)
      switchTab('workers');
    };

    // Initialize the WebSocket for real-time dashboard data
    function initDashboardWebSocket() {
      const wsProtocol = (location.protocol === 'https:') ? 'wss:' : 'ws:';
      const wsUrl = `${wsProtocol}//${location.host}/api/ws/dashboard`;
      dashboardSocket = new WebSocket(wsUrl);

      dashboardSocket.onopen = () => {
        console.log("WebSocket connected!");
      };

      dashboardSocket.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);

          // 1. Update Stats
          if (msg.stats) {
            document.getElementById('ml_tasks_count').textContent = msg.stats.ml_tasks_count || 0;
            document.getElementById('processing_count').textContent = msg.stats.processing_count || 0;
            document.getElementById('active_workers').textContent = msg.stats.active_workers_count || 0;
          }

          // 2. Update Workers
          if (msg.workers) {
            const tableBody = document.getElementById("workers_table");
            tableBody.innerHTML = "";

            let i = 1;
            for (const workerId of Object.keys(msg.workers)) {
              const w = msg.workers[workerId];
              const statusLower = (w.status || "").toLowerCase();

              let statusClass = "bg-red-500 text-white";
              let tooltipText = "Unknown status";

              if (statusLower.includes("busy")) {
                statusClass = "bg-orange-500 text-white";
                tooltipText = "This worker is actively processing tasks";
              } else if (statusLower.includes("idle")) {
                statusClass = "bg-green-500 text-white";
                tooltipText = "This worker is idle and ready for tasks";
              }

              const lastActive = w.last_heartbeat
                ? new Date(w.last_heartbeat * 1000).toLocaleString("en-US", {
                    hour: "numeric",
                    minute: "numeric",
                    second: "numeric",
                    hour12: true
                  })
                : "N/A";

              const row = `
                <tr>
                  <td class="py-2 px-4 border-b">${i}</td>
                  <td class="py-2 px-4 border-b">${workerId}</td>
                  <td class="py-2 px-4 border-b relative group">
                    <span class="${statusClass} px-3 py-1 rounded-full inline-block">
                      ${w.status || "Unknown"}
                    </span>
                    <span class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2
                                 px-2 py-1 bg-gray-700 text-white text-xs rounded shadow 
                                 opacity-0 group-hover:opacity-100 transition-opacity 
                                 pointer-events-none z-10">
                      ${tooltipText}
                    </span>
                  </td>
                  <td class="py-2 px-4 border-b">${lastActive}</td>
                </tr>
              `;
              tableBody.innerHTML += row;
              i++;
            }
          }
          // 3. If you also sent tasks data, you could update requests table similarly...

        } catch (error) {
          console.error("Error parsing WebSocket message:", error);
        }
      };

      dashboardSocket.onclose = (event) => {
        console.warn("WebSocket closed:", event.reason);
        // Optionally attempt to reconnect after a delay
        setTimeout(() => initDashboardWebSocket(), 3000);
      };

      dashboardSocket.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
    }

    // Switch between the two tabs
    function switchTab(tabName) {
      const workersTabBtn = document.getElementById('tab-workers');
      const requestsTabBtn = document.getElementById('tab-requests');
      const workersSection = document.getElementById('workers_section');
      const requestsSection = document.getElementById('requests_section');

      if (tabName === 'workers') {
        workersTabBtn.classList.add('border-black', 'text-black');
        workersTabBtn.classList.remove('border-transparent', 'text-gray-500');

        requestsTabBtn.classList.remove('border-black', 'text-black');
        requestsTabBtn.classList.add('border-transparent', 'text-gray-500');

        workersSection.classList.remove('hidden');
        requestsSection.classList.add('hidden');
      } else {
        requestsTabBtn.classList.add('border-black', 'text-black');
        requestsTabBtn.classList.remove('border-transparent', 'text-gray-500');

        workersTabBtn.classList.remove('border-black', 'text-black');
        workersTabBtn.classList.add('border-transparent', 'text-gray-500');

        requestsSection.classList.remove('hidden');
        workersSection.classList.add('hidden');

        // Fetch the queued requests only when switching to this tab
        getQueuedRequests();
      }
    }

    // Fetch the last N queued requests (where N is chosen in dropdown) and show them
    async function getQueuedRequests() {
      try {
        const select = document.getElementById('request_limit');
        const limit = select.value;

        const response = await fetch('/api/queued_requests?limit=' + limit);
        if (!response.ok) throw new Error('Failed to fetch queued requests');
        const tasks = await response.json();

        const requestsTableBody = document.getElementById("requests_table");
        requestsTableBody.innerHTML = "";

        tasks.forEach((task, index) => {
          const rowNumber = index + 1;
          const taskId = task.task_id || "N/A";
          const status = task.status || "unknown";

          // Show queued_time in 12-hour format
          const queuedTime = task.queued_time
            ? new Date(task.queued_time * 1000).toLocaleString("en-US", {
                hour: "numeric",
                minute: "numeric",
                second: "numeric",
                hour12: true
              })
            : "N/A";

          const row = `
            <tr>
              <td class="py-2 px-4 border-b">${rowNumber}</td>
              <td class="py-2 px-4 border-b">${taskId}</td>
              <td class="py-2 px-4 border-b">${status}</td>
              <td class="py-2 px-4 border-b">${queuedTime}</td>
            </tr>
          `;
          requestsTableBody.innerHTML += row;
        });
      } catch (error) {
        console.error('Error fetching queued requests:', error);
      }
    }

    // Attempt to fetch a task by ID, then show in a modal popup if found
    async function getTask() {
      const taskId = document.getElementById('task_id').value.trim();
      if (!taskId) {
        alert('Please enter a Task ID');
        return;
      }

      try {
        const response = await fetch(`/api/task/${taskId}`);
        if (!response.ok) {
          throw new Error('Task not found');
        }
        const data = await response.json();
        // Show the data in a modal
        showTaskModal(data);
      } catch (error) {
        console.error('Error fetching task:', error);
        alert('Task not found');
      }
    }

    // Show modal with JSON data
    function showTaskModal(jsonData) {
      const modal = document.getElementById("taskModal");
      const taskJsonElement = document.getElementById("taskJson");

      // Pretty-print the JSON
      taskJsonElement.textContent = JSON.stringify(jsonData, null, 2);

      // Display the modal
      modal.classList.remove("hidden");
    }

    // Hide modal
    function hideTaskModal() {
      const modal = document.getElementById("taskModal");
      modal.classList.add("hidden");
    }

    // Copy JSON content to clipboard
    function copyTaskJson() {
      const taskJsonElement = document.getElementById("taskJson");
      const textToCopy = taskJsonElement.textContent;

      navigator.clipboard.writeText(textToCopy)
        .then(() => {
          alert('JSON copied to clipboard!');
        })
        .catch((err) => {
          console.error('Failed to copy:', err);
        });
    }
  </script>
</body>
</html>
"""

    def serve(self):
        uvicorn.run(self.app, host=self.host, port=self.port)
