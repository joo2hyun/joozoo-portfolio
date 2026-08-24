// Fill these in after creating your Supabase project:
// Supabase Dashboard → Project Settings → API
const SUPABASE_URL = 'https://gycjzxcvfaslnxvldvbb.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd5Y2p6eGN2ZmFzbG54dmxkdmJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODYwNTE0MjAsImV4cCI6MjEwMTYyNzQyMH0.-KJ9oRbp8N7bAg-lqU8I4mk6Nhrdy1aXShlppwK7I4U';

const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
