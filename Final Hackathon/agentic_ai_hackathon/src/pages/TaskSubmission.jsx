// LinkedInForm.tsx
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import axiosInstance from '@/api/axiosInstance';
import { useSelector } from 'react-redux';
import { useState } from 'react';
import { ClipLoader, PacmanLoader } from 'react-spinners';
import { toast } from 'react-toastify';
import EvaluationFeedback from '@/components/custom_components/EvaluationFeedback';
import FeedbackDisplay from '@/components/custom_components/feedback_display';

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
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState({ title: {}, result: {} });
  const { user_id } = useSelector((state) => state.auth.user);
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm({
    resolver: zodResolver(linkedinSchema),
  });

  const onSubmit = async (data) => {
    try {
      setLoading(true);
      console.log('clicked');
      const title = await axiosInstance.post(
        'http://localhost:8000/get-title',
        {
          url: data.linkedinUrl,
        },
      );

      if (title?.statusText === 'OK') {
        const res = await axiosInstance.post('http://localhost:8000/verify', {
          article_title: title?.data?.title,
          user_id: user_id,
          url: data?.linkedinUrl,
        });
        console.log({ res });
        setReport(res?.data);
        toast.success('task completed successfully');
      }
    } catch (error) {
      console.error(error);
      toast.error('Error occurred');
    } finally {
      setLoading(false);
      reset();
    }
  };

  console.log({ report });

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)} className="mt-10 space-y-4">
        <span className="text-center text-3xl font-bold">Submission Form</span>
        <label className="my-2 block">
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

        {loading ? (
          <span className="flex items-center gap-3">
            <ClipLoader /> Ai Agent is verifying the task
          </span>
        ) : (
          <button
            type="submit"
            className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
            disabled={loading}
          >
            Submit
          </button>
        )}
      </form>
      {/* {report && <EvaluationFeedback data={report} />} */}
      <FeedbackDisplay data={report || ''} />
    </>
  );
};

export default LinkedInForm;
