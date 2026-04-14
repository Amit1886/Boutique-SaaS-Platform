import { useAuthStore } from "../stores/authStore";

export default function ProfilePage() {
  const user = useAuthStore((s) => s.user);
  return (
    <div className="space-y-5 fade-in">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Profile</div>
        <div className="mt-2 text-sm opacity-70">User account + saved personality.</div>
      </div>
      <div className="rounded-2xl border border-base-300 bg-base-100 p-6">
        {!user ? (
          <div className="opacity-70">Login required.</div>
        ) : (
          <div className="space-y-2">
            <div>
              <span className="opacity-70">Email:</span> <span className="font-semibold">{user.email}</span>
            </div>
            <div>
              <span className="opacity-70">Name:</span> <span className="font-semibold">{user.name}</span>
            </div>
            <div>
              <span className="opacity-70">Language:</span> <span className="font-semibold">{user.language}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

