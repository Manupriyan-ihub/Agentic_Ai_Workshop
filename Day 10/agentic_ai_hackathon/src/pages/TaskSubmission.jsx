// LinkedInForm.tsx
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

// 1. Zod schema for LinkedIn URL validation
const linkedinSchema = z.object({
  linkedinUrl: z
    .string()
    .url('Please enter a valid URL')
    .regex(
      /^https:\/\/(www\.)?linkedin\.com\/.*$/,
      'Must be a valid LinkedIn URL',
    ),
});

// 3. Component
const LinkedInForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(linkedinSchema),
  });

  const onSubmit = (data) => {
    console.log('Submitted LinkedIn URL:', data.linkedinUrl);
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      className="max-w-md space-y-4 p-4 shadow-2xl"
    >
      <label className="block">
        <span className="text-gray-700">LinkedIn URL</span>
        <input
          type="text"
          {...register('linkedinUrl')}
          className="mt-1 block w-full rounded-md border border-gray-300 p-2"
          placeholder="https://www.linkedin.com/in/your-profile"
        />
        {errors.linkedinUrl && (
          <p className="mt-1 text-sm text-red-500">
            {errors.linkedinUrl.message}
          </p>
        )}
      </label>

      <button
        type="submit"
        className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
      >
        Submit
      </button>
    </form>
  );
};

export default LinkedInForm;
