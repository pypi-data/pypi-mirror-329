function WebhookDashboard() {
  const [activeTab, setActiveTab] = React.useState("webhooks");
  const [webhooks, setWebhooks] = React.useState([]);
  const [events, setEvents] = React.useState([]);
  const [url, setUrl] = React.useState("");
  const [channel, setChannel] = React.useState("Project");
  const [eventFilter, setEventFilter] = React.useState(".*");
  const [formId, setFormId] = React.useState("15672913");
  const [formPayload, setFormPayload] = React.useState(null);
  const [responseData, setResponseData] = React.useState("");

  React.useEffect(() => {
    fetchWebhooks().catch((error) =>
      console.error("Error fetching webhooks:", error),
    );
    fetchWebhookEvents().catch((error) =>
      console.error("Error fetching webhook events:", error),
    );

    const socket = io();
    socket.on("new_webhook_event", (event) => {
      setEvents((prevEvents) => [event, ...prevEvents]);
    });

    return () => socket.disconnect();
  }, []);

  async function fetchWebhooks() {
    const response = await fetch("/api/view_webhooks");
    const data = await response.json();
    setWebhooks(data.webhooks || []);
  }

  async function fetchWebhookEvents() {
    const response = await fetch("/api/webhook_events");
    const data = await response.json();
    setEvents(data.events || []);
  }

  async function fetchFormData() {
    if (!formId) return;
    try {
      const response = await fetch(`/api/get_form/${formId}`);
      const data = await response.json();
      setFormPayload(data);
    } catch (error) {
      console.error("Failed to fetch form:", error);
    }
  }

  async function registerWebhook() {
    await fetch("/api/register_webhook", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, channel, event: eventFilter }),
    });
    fetchWebhooks();
  }

  async function unregisterWebhook(hookId) {
    await fetch("/api/unregister_webhook", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ hook_ids: [hookId] }),
    });
    fetchWebhooks();
  }

  function updateField(section, key, value) {
    setFormPayload((prev) => ({
      ...prev,
      form: {
        ...prev.form,
        [section]: {
          ...prev.form[section],
          [key]: value,
        },
      },
    }));
  }

  async function sendPutRequest() {
    try {
      const response = await fetch("/api/update_form", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ formId, form: formPayload }),
      });

      const result = await response.json();
      setResponseData(JSON.stringify(result, null, 2));
    } catch (error) {
      setResponseData(`Error: ${error.message}`);
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Webhook & Form Manager</h1>

      {/* Tabs Navigation */}
      <div className="flex border-b mb-4">
        {["webhooks", "formEditor", "webhookEvents"].map((tab) => (
          <button
            key={tab}
            className={`px-4 py-2 ${
              activeTab === tab
                ? "border-b-2 border-blue-500 font-bold"
                : "text-gray-600"
            }`}
            onClick={() => setActiveTab(tab)}
          >
            {tab === "webhooks"
              ? "Manage Webhooks"
              : tab === "formEditor"
                ? "Form Editor"
                : "Webhook Events"}
          </button>
        ))}
      </div>

      {/* Webhooks Tab */}
      {activeTab === "webhooks" && (
        <div>
          <h2 className="text-lg font-semibold mb-4">Registered Webhooks</h2>

          <div className="border rounded-lg p-4 bg-gray-50">
            {webhooks.length === 0 ? (
              <p className="text-gray-500 text-center">
                No webhooks registered.
              </p>
            ) : (
              <ul className="space-y-2">
                {webhooks.map((hook) => (
                  <li
                    key={hook.hookId}
                    className="flex flex-wrap items-center justify-between gap-4 p-3 border rounded bg-white shadow-sm"
                  >
                    <div className="flex-1">
                      <p className="font-medium">{hook.url}</p>
                      <p className="text-sm text-gray-600">
                        {hook.channel}: {hook.eventFilter}
                      </p>
                      <p className="text-sm text-gray-500">
                        Expires: {formatLeaseEnd(hook.leaseEnd)}
                      </p>
                    </div>

                    <button
                      className="bg-red-500 text-white px-4 py-1.5 rounded-lg hover:bg-red-600 transition"
                      onClick={() => unregisterWebhook(hook.hookId)}
                    >
                      Unregister
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <h2 className="text-lg font-semibold mt-6 mb-3">
            Register a Webhook
          </h2>
          <input
            type="text"
            placeholder="Webhook URL"
            className="p-2 border rounded w-full mb-2"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <select
            className="p-2 border rounded w-full mb-2"
            value={channel}
            onChange={(e) => setChannel(e.target.value)}
          >
            {[
              "Project",
              "Status",
              "Phase",
              "Form",
              "File",
              "Tag",
              "Action",
            ].map((ch) => (
              <option key={ch} value={ch}>
                {ch}
              </option>
            ))}
          </select>
          <input
            type="text"
            placeholder="Event Regex Filter"
            className="p-2 border rounded w-full mb-2"
            value={eventFilter}
            onChange={(e) => setEventFilter(e.target.value)}
          />
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded w-full"
            onClick={registerWebhook}
          >
            Register Webhook
          </button>
        </div>
      )}

      {/* Form Editor Tab */}
      {activeTab === "formEditor" && (
        <div>
          <h2 className="text-lg font-semibold mb-3">
            Edit Form & Send PUT Request
          </h2>
          <input
            type="text"
            placeholder="Enter Form ID"
            className="p-2 border rounded w-full mb-2"
            value={formId}
            onChange={(e) => setFormId(e.target.value)}
          />
          <button
            className="bg-gray-500 text-white px-4 py-2 rounded w-full mb-3"
            onClick={fetchFormData}
          >
            Load Form
          </button>

          {formPayload ? (
            Object.keys(formPayload.form.fields).map((field) => (
              <div key={field} className="mb-2">
                <label className="block text-sm font-semibold">{field}</label>
                <input
                  type="text"
                  className="p-2 border rounded w-full"
                  value={formPayload.form.fields[field]}
                  onChange={(e) => updateField("fields", field, e.target.value)}
                />
              </div>
            ))
          ) : (
            <p className="text-gray-500">Click "Load Form" to fetch data.</p>
          )}

          <button
            className="bg-green-500 text-white px-4 py-2 rounded w-full"
            onClick={sendPutRequest}
          >
            Send PUT Request
          </button>
          <h3 className="text-md font-semibold mt-3">Response:</h3>
          <pre className="p-2 bg-gray-100 border rounded mt-2 text-sm">
            {responseData || "Awaiting response..."}
          </pre>
        </div>
      )}

      {/* Webhook Events Tab */}
      {activeTab === "webhookEvents" && (
        <div>
          <h2 className="text-lg font-semibold mb-3">Webhook Events</h2>
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded mb-2"
            onClick={fetchWebhookEvents}
          >
            Refresh Events
          </button>
          <ul className="border rounded p-2 bg-gray-50">
            {events.length === 0 ? (
              <p className="text-gray-500">No webhook events received yet.</p>
            ) : (
              events.map((event, index) => (
                <li key={index} className="border-b p-2">
                  <pre className="bg-gray-100 p-2 rounded text-xs">
                    {JSON.stringify(event, null, 2)}
                  </pre>
                </li>
              ))
            )}
          </ul>
        </div>
      )}
    </div>
  );
}

function formatLeaseEnd(leaseEnd) {
  const now = Date.now();
  const leaseEndDate = new Date(leaseEnd);
  const timeRemaining = leaseEnd - now;

  if (timeRemaining <= 0) {
    return {
      readableDate: leaseEndDate.toUTCString(),
      timeUntilExpiration: "Expired",
    };
  }

  const seconds = Math.floor(timeRemaining / 1000) % 60;
  const minutes = Math.floor(timeRemaining / (1000 * 60)) % 60;
  const hours = Math.floor(timeRemaining / (1000 * 60 * 60)) % 24;
  const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));

  let friendlyTime = "";
  if (days > 0) friendlyTime += `${days}d `;
  if (hours > 0) friendlyTime += `${hours}h `;
  if (minutes > 0) friendlyTime += `${minutes}m `;
  if (seconds > 0 || friendlyTime === "") friendlyTime += `${seconds}s`;

  return friendlyTime.trim();
}

ReactDOM.createRoot(document.getElementById("root")).render(
  <WebhookDashboard />,
);
